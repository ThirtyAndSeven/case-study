from ..emmy_case_study.utils import (
    create_dict_from_json_like_string,
    find_specific_value_from_nested_dicts,
)


def test_create_dict_from_json_like_string():
    test_dict = create_dict_from_json_like_string(
        '{"driven_distance" : 7000, "pizzas_delivered" : 3}'
    )
    assert type(test_dict) == dict
    assert test_dict['driven_distance'] == 7000
    assert test_dict['pizzas_delivered'] == 3


def test_find_specific_value_from_nested_dicts():
    normal_dict = {"driven_distance": 7000, "pizzas_delivered": 3}
    nested_dict = {
        "maintenance": {},
        "weather": "okayish",
        "metrics": {"driven_distance": 3500, "pizzas_delivered": 3},
    }
    assert find_specific_value_from_nested_dicts(normal_dict, "driven_distance") == 7000
    assert find_specific_value_from_nested_dicts(nested_dict, "driven_distance") == 3500
