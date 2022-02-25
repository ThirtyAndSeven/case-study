# ---
# jupyter:
#   jupytext:
#     formats: notebooks///ipynb,scripts///py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3.9.6 64-bit
#     language: python
#     name: python3
# ---

# %% [markdown]
# # EMMY CASE STUDY

# %%
import datetime
import json
import pathlib

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from emmy_case_study import utils

# %% [markdown]
# Import data and create respective dataframes

# %%
current_path = pathlib.Path()
project_path = current_path.absolute().parent
data_path_for_cars = project_path / 'data/cars.csv'
data_path_for_mobility_events = project_path / 'data/mobility_event_data.csv'
data_path_for_map = project_path / '.map/map.png'


# %%
df_events = pd.read_csv(data_path_for_mobility_events, header=0)
df_cars = pd.read_csv(data_path_for_cars, header=0)

# %% [markdown]
# ## Basic data exploration and data cleaning
#
# First, lets get a feel for the data. I want to look for typical behaviour in column data. After That we can check if any critical data is missing so we can start thinking about possible data cleaning processes.

# %%
df_events.head(30)

# %%
df_cars.head(30)

# %% [markdown]
# As expected, many columns are critical for precise evaluation. There are is also expected missing data like missing ride ids for maintenance events, as well as missing driven distance, which only occurs in ride_end events. First I want to check if there are any missing events in the head part of this data frame. For now we can see a lot of reservations created, as well as ride starts and ends, or maintenance events. Also we want to check if there are any other vehicle types. Later on I will join both tables to explore differences between both vehicle types.

# %%
df_cars['vehicle_type'].unique()

# %%
unique_events = df_events['event'].unique()
print(unique_events)

# %% [markdown]
# And of course there was one event hiding. Event cancelation are very important metrics which I will explore furthermore in a later part.
#
# For now I want to check if there are any missing data in critical columns.

# %%
for header in df_events.columns.values:
    df_column = df_events[header]
    print(f"Null values in column {header}: {df_column.isnull().values.any()}")

for header in df_cars.columns.values:
    df_column = df_cars[header]
    print(f"Null values in column {header}: {df_column.isnull().values.any()}")

# %% [markdown]
# It seems like there are no null values in the critical columns. If all of your actual data looks like this: kudos! We dont need to clean any data in that regard.
# Next I want to check if there are any unexpacted or impossible values in any of the ids, geological data as well as battery percentages.
#
# ### Checking for rogue ids

# %%
print(
    f"Min and max vehicle_id in the vehicles table: {df_cars['vehicle_id'].min()}, {df_cars['vehicle_id'].max()}"
)
print(
    f"Min and max vehicle_id in the events table: {df_events['vehicle_id'].min()}, {df_events['vehicle_id'].max()}"
)


# %% [markdown]
# ## Cast event times to datetimes

# %%
df_events["event_time"] = pd.to_datetime(df_events["event_time"])
df_events["year"] = df_events["event_time"].dt.year
df_events["month"] = df_events["event_time"].dt.month
df_events["day"] = df_events["event_time"].dt.day
df_events["hour"] = df_events["event_time"].dt.hour
df_events["weekday"] = df_events["event_time"].apply(datetime.datetime.weekday)

# %% [markdown]
# ### Checking for unusual battery values
#
# We don't expect anything above 100% or underneath 0%. I will print the lowest and highest values. Just to be sure.

# %%
print(
    f"Min and max battery_pct in the events table: {df_events['battery_pct'].min()}, {df_events['battery_pct'].max()}"
)

# %% [markdown]
# Well, at least we don't have any values below 0% but 255 battery percentage seems unusual. It could be a status code, but I want to look for more examples.

# %%
df_events[df_events['battery_pct'] > 100]

# %% [markdown]
# I will remove those columns for the sake of this case study. Usually I would ask around if there is any hidden meaning behind this specific value. Interestingly enough, we can find a lot of reservations and ride starts for the respective vehicle_id. So at least I can conclude that these specific vehicles are still operational, but this could lead to problems from an operational standpoint. Costumers could book unoperational vehicles, which could lead to a less then perfect customer experience. Lets join both tables together and see if its a vehicle-specific problem.

# %%
df_events = df_events.join(df_cars.set_index('vehicle_id'), how='left', on='vehicle_id')

# %% [markdown]
# Lets check for unsual battery percentages with regard to the vehicle type.

# %%
df_events[df_events['battery_pct'] > 100]

# %% [markdown]
# We can already see two different vehicle_types. Usually I would ask around if there is any technical meaning behind this number. I will delete the specific rows for the sake of this case study.

# %%
df_events = df_events[df_events['battery_pct'] <= 100]

# %% [markdown]
# Now I'd like to check for faulty geolocations. We already verified the nonexistence of null values. So looking for min-max-values should suffice.

# %%
print(
    f"Min and max value in latitude: {df_events['latitude'].min()}, {df_events['latitude'].max()}"
)
print(
    f"Min and max value in longitude: {df_events['longitude'].min()}, {df_events['longitude'].max()}"
)


# %% [markdown]
# A quick sanity check suffices to see that the geolocation ranges between Stuttgart, Berlin and Vienna. So we have an expected range of geo data, which indicates no necessity of cleaning the data in that regard. Sadly none of our observed vehicles has a vacation on an tropical island :)
#
# Last but not least I will extract the driven_distance value from the comment column and will add another column with the sole integer value. This will enable future comparisons such as expected battery consumption based on location and the driven distance.

# %%
df_events["comment"] = df_events["comment"].fillna("{}")
df_events["comment"] = df_events["comment"].apply(json.loads)

# %%


df_events["driven_distance"] = df_events["comment"].apply(
    lambda x: utils.find_value_in_nested_dicts(x, "driven_distance")
)

# %% [markdown]
#
# ## Data Analysis

# %% [markdown]
# ## Basic KPIs
# At first I want to get a measurement in performance behaviour and its distribution. Also, I want to know if we can beat a trailing average, but my data only spans over two months. Because of the seasonal nature of Emmy's business, I would consider comparing the usage performance from past years. In this case I just measured the mean from my available data.

# %%
for event_type in ("reservation_creation", "ride_start", "reservation_cancelation"):
    df_count_pivot_table = pd.pivot_table(
        df_events[["event", "year", "month", "day"]].where(
            df_events["event"] == f'{event_type}'
        ),
        columns=["event"],
        index=["year", "month", "day"],
        aggfunc=np.count_nonzero,
    )

    mu_count_events = df_count_pivot_table[event_type].mean()
    sigma_count_events = np.sqrt(df_count_pivot_table[event_type].var())
    risk_count_events = df_count_pivot_table[event_type].quantile(q=0.05)

    plot_hist_count_events = df_count_pivot_table.plot.hist(
        xlabel="number of events", bins=20, figsize=(16, 9), grid=True
    )
    plot_hist_count_events.axvline(x=mu_count_events, color="black", label="mean")
    plot_hist_count_events.axvline(
        x=risk_count_events, color="red", linestyle="--", label="0.05 Percentile"
    )
    plot_hist_count_events.legend()

    plot_line_count_events = df_count_pivot_table.plot(figsize=(16, 9), grid=True)
    plot_line_count_events.axhline(y=mu_count_events, color="black", label="mean")
    plot_line_count_events.axhline(
        y=risk_count_events, color="red", linestyle="--", label="0.05 Percentile"
    )
    plot_line_count_events.legend()


# %% [markdown]
# Can we create value from this? Probably not, but at least we can understand our business a little bit better. The Usage seems to be steady around the the daily mean. The daily reservations fluctuate steadily at around alightly above 18000 reservations a day and doesnt seem to move much above 20000 or underneath 16000 reservations. The actual usage of our scooters seems to move about around 12500 rides a day, staying in a range of 10000 to 14000 per day and peaking at 16000 per day.
#
# Also, we may see a usage pattern in regards to the weekdays. I was already told about the dynamic prices project and the weekdays with their respective usage may seem like an obvious choice as part of a model. Daytime, location and fleet capacity at the respective location could also be model parameters. We could also incorporate some kind of recommender system to predict a destination or the battery usage from our user behaviour.

# %%
df_weekday_count_pivot_table = (
    pd.pivot_table(
        df_events[["event", "year", "month", "day", "weekday"]].where(
            df_events["event"] == "ride_start"
        ),
        columns=["event"],
        index=["year", "month", "day", "weekday"],
        aggfunc=np.count_nonzero,
    )
    .groupby("weekday")
    .mean()
)

plot_usage_by_weekday = df_weekday_count_pivot_table.plot.bar(
    figsize=(16, 9), grid=True, title="Mean scooter rides per weekday"
)
plot_usage_by_weekday.axhline()

# %% [markdown]
# In this figure we can see the distribution of rides per weekday from 0 = monday to 6 = sunday. It is very surprising to see significant less usage on mondays. I would also expect to see most usage in the morning (e.g. commuting to work) or the evening. Emmy's service as an alternative to cab services would also lead to an increased usage in the evening (dober usage hopefully). Let's get a feeling for the mean hourly usage and compare them among the weekdays.

# %%
df_hourly_usage_count_pivot_table = (
    pd.pivot_table(
        df_events[["event", "year", "month", "day", "hour", "weekday"]],
        columns=["event"],
        index=["year", "month", "day", "hour", "weekday"],
        aggfunc=np.count_nonzero,
    )
    .groupby(["weekday", "hour"])
    .mean()
)
df_hourly_usage_count_pivot_table.plot(
    figsize=(16, 9),
    title="Mean scooter rides per hour on weekdays",
    xticks=range(0, 168, 6),
    rot=90,
    grid=True,
)

# %% [markdown]
# Now this figure is telling a story! We can learly see an increased usage in the morning and evening. Clearly customers use our service to commute to and from work. We can also see an increase friday and saturday night. So this data shows a pattern and should be very useful for dynamic pricing systems. It should also be very useful for operations, so we can manage when we should dispatch most of the maintenance crew. I will plot log scaled figure to compare "ride_end" events with maintenance events to get a better picture
#
# ## Operations

# %%
df_hourly_usage_count_pivot_table = (
    pd.pivot_table(
        df_events[["event", "year", "month", "day", "hour", "weekday"]].where(
            np.logical_or(
                df_events["event"] == "maintenance_start",
                df_events["event"] == "ride_end",
            )
        ),
        columns=["event"],
        index=["year", "month", "day", "hour", "weekday"],
        aggfunc=np.count_nonzero,
    )
    .groupby(["weekday", "hour"])
    .mean()
)
df_hourly_usage_count_pivot_table.plot(
    figsize=(16, 9),
    title="Maintenance response on usage spike",
    xticks=range(0, 168, 6),
    ylabel="log scaled number of events",
    logy=True,
    rot=90,
    grid=True,
)

# %%
df_ride_start_to_end_merge = pd.merge(
    df_events[df_events["event"] == "ride_start"],
    df_events[df_events["event"] == "ride_end"],
    on=["ride_id", "ride_id"],
)
df_ride_start_to_end_merge["battery_pct_used"] = (
    df_ride_start_to_end_merge["battery_pct_x"]
    - df_ride_start_to_end_merge["battery_pct_y"]
)


# %% [markdown]
# It looks like there are some cases, which seem to indicate, that some customers might charge their scooter.

# %%
df_ride_start_to_end_merge[df_ride_start_to_end_merge["battery_pct_used"] < 0]

# %%
mu_battery_pct_used = df_ride_start_to_end_merge["battery_pct_used"].mean()
sigma_battery_pct_used = np.sqrt(df_ride_start_to_end_merge["battery_pct_used"].var())
risk_battery_pct_used = df_ride_start_to_end_merge["battery_pct_used"].quantile(q=0.95)

plot_battery_delta = df_ride_start_to_end_merge["battery_pct_used"].plot.hist(
    bins=100,
    figsize=(16, 9),
    title="Distribution of battery_pct used per ride",
    xlabel="battery_pct used",
    grid=True,
)

plot_text = (
    f'mu = {round(mu_battery_pct_used, 2)}'
    f'\nsigma = {round(sigma_battery_pct_used, 2)}'
    f'\n95th percentile = {round(risk_battery_pct_used, 2)}'
)
plot_battery_delta.text(25, 30000, plot_text)

plot_battery_delta.axvline(x=mu_battery_pct_used, color="black", label="mu")
plot_battery_delta.axvline(
    x=risk_battery_pct_used, color="red", linestyle="--", label="95th percentile"
)

plot_battery_delta.legend()


# %% [markdown]
# Using this figure I can create a guideline system. I should probably also consider the vehicle type, but for now I will generalize a system with both vehicle types in mind. Assuming our custors won't charge their rented vehicle during their trip, we can assign a warning state for every vehicle using the mean battery usage and the 95th percentile of our data.

# %%
def apply_color(val: float, warning_limit: float, critical_limit: float) -> str:
    if val <= warning_limit:
        color = "yellow"
    elif val <= critical_limit:
        color = "red"
    else:
        color = "black"
    return


df_critical_batteries = df_events[
    np.logical_and(
        df_events["event"] == "ride_end",
        df_events["battery_pct"] <= mu_battery_pct_used,
    )
]

box = (
    df_critical_batteries["longitude"].min(),
    df_critical_batteries["longitude"].max(),
    df_critical_batteries["latitude"].min(),
    df_critical_batteries["latitude"].max(),
)

_, heatmap = plt.subplots(figsize=(16, 9))
berlin_map = plt.imread(data_path_for_map)

heatmap.hexbin(
    x=df_critical_batteries["longitude"],
    y=df_critical_batteries["latitude"],
    zorder=1,
    cmap="inferno",
    alpha=0.3,
    lw=0,
)
heatmap.set_xlim(box[0], box[1])
heatmap.set_ylim(box[2], box[3])
heatmap.imshow(berlin_map, extent=box, aspect="equal")
f"The long/lat bounderies are: {box}"

# %% [markdown]
# ## Churn Rates
# In an ideal world we want to catch our customers from the beginning of their journey until they are safe and sound at their friends and families, at work or wherever our costumers choose to go. So lets disect the churn rate of our costumer behaviour.

# %%
df_churn_count_pivot_table = pd.DataFrame()
for event_type in ("reservation_creation", "ride_start", "reservation_cancelation"):
    df_churn_count_pivot_table[event_type] = pd.pivot_table(
        df_events[["event", "year", "month", "day"]].where(
            df_events["event"] == f'{event_type}'
        ),
        columns=["event"],
        index=["year", "month", "day"],
        aggfunc=np.count_nonzero,
    )

df_churn_count_pivot_table.plot.box(figsize=(16, 9), grid=True, title="")

# %%
df_pivot = pd.pivot_table(
    df_events,
    values=["battery_pct", "driven_distance"],
    index=["year", "month", "event"],
    aggfunc=np.mean,
)
