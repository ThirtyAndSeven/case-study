import json


def create_dict_from_json_like_string(json_like_string: str) -> dict:
    """Create a dict from a json-like string.

    Args:
        json_like_string (str): string that need to be jsonified.

    Returns:
        dict: From the json string created dict.
    """
    return json.loads(json_like_string)


def find_specific_value_from_nested_dicts(
    comments_dict: dict, key_to_find: str, value=None
):
    for key in comments_dict.keys():
        if type(comments_dict[key]) == dict:
            value = find_specific_value_from_nested_dicts(
                comments_dict[key], key_to_find, value
            )
        elif key == key_to_find:
            value = comments_dict[key]
    return value
