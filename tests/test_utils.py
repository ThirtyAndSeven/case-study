from ..emmy_case_study.utils import find_value_in_nested_dicts


def test_find_specific_value_from_nested_dicts():
    normal_dict = {"driven_distance": 7000, "pizzas_delivered": 3}
    nested_dict = {
        "maintenance": {},
        "weather": "okayish",
        "metrics": {"driven_distance": 3500, "pizzas_delivered": 3},
    }
    assert find_value_in_nested_dicts(normal_dict, "driven_distance") == 7000
    assert find_value_in_nested_dicts(nested_dict, "driven_distance") == 3500
