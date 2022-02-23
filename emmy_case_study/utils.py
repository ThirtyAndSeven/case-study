from typing import Any


def find_value_in_nested_dicts(
    dict_to_search: dict, key_to_find: str, data: Any = None
) -> Any:
    """Searches for a value for a specific key within a potential nested dict.

    Args:
        dict_to_search (dict): The dict which will be searched.
        key_to_find (str): search goal within the nested dict.

    Returns:
        data (Any): the searched value for the key input
    """
    if dict_to_search:
        for key, val in dict_to_search.items():
            if isinstance(val, dict):
                data = find_value_in_nested_dicts(val, key_to_find)
            elif key == key_to_find:
                data = val
                break
    return data if data else None
