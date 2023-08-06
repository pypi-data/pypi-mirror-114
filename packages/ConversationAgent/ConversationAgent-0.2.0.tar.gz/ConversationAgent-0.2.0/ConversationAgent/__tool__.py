def get_value_from_dict_by_multi_name(d: dict, names: [str], default=None):
    for name in names:
        if name in d:
            return d[name]
    return default
