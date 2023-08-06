from copy import deepcopy


def remove_key(value: dict, removed_key='self') -> dict:
    if removed_key in value:
        value.pop(removed_key)
    return value


def package_data(dict_data: dict, replace_keys: dict = None) -> dict:
    if replace_keys is None:
        replace_keys = dict()
    new_dict = deepcopy(dict_data)

    for k, v in dict_data.items():
        if v is None:
            new_dict.pop(k)
        if k in replace_keys:
            new_dict[replace_keys[k]] = new_dict.pop(k)
    return new_dict
