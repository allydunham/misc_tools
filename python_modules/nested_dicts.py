#!/usr/bin/env python3
"""
Nested dictionary update function
"""
import collections
import copy

def nested_merge(*args):
    """Recursively merges dictionaries. The dicts provided as later arguments take priority"""
    if len(args) > 2:
        return nested_merge(args[0], nested_merge(*args[1:]))
    elif len(args) == 2:
        dict1 = copy.deepcopy(args[0])
        dict2 = args[1]
        for key, value in dict2.items():
            if isinstance(value, collections.Mapping):
                if isinstance(dict1.get(key, {}), collections.Mapping):
                    dict1[key] = nested_merge(dict1.get(key, {}), value)
                else:
                    dict1[key] = value
            else:
                dict1[key] = value

        return dict1
    else:
        # Case of one supplied dict
        return copy.deepcopy(args[0])

def nested_keys(dic, inc_dict_keys=False):
    """Return a list of all keys in a nested dictionary"""
    keys = []
    for key, value in dic.items():
        if isinstance(value, collections.Mapping):
            keys.extend(nested_keys(value))
            if inc_dict_keys:
                keys.append(key)
        else:
            keys.append(key)

    return keys

if __name__ == "__main__":
    DICT1 = {'k1':1, 'k2':[1, 2, 3], 'k3':{'kk1':2, 'kk2':'str'}}
    DICT2 = {'k1':2, 'k2':'string', 'k3':{'kk1':3}, 'k4':'another str'}
    DICT3 = {'k1':3, 'k4':'extra'}
    DICT4 = {'k1':1, 'k2':{'kk3':{'kkk1':1, 'kkk2':2, 'kkk3':{'kkkk1':'final level'}}},
             'k3':{'kk1':2, 'kk2':{'kkk4':4}}}
    print(nested_merge(DICT1, DICT2))
    print(nested_merge(DICT1, DICT2, DICT3))
    print(nested_merge(DICT1, DICT4))
    print(nested_keys(DICT4))
