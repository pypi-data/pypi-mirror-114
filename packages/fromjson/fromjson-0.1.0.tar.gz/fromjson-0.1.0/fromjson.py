import json
from typing import get_type_hints


def __is_primitive(t):
    if t is bool:
        return True
    elif t is str:
        return True
    elif t is int:
        return True
    elif t is float:
        return True
    elif t is dict:
        return True
    elif t is list:
        return True
    else:
        try:
            if t.__origin__ is dict:
                return True
        except AttributeError:
            return False
        try:
            if t.__origin__ is list:
                return True
        except AttributeError:
            return False
        return False


def fromjson(cls):
    def __from_json(d):
        constructor_args = {}
        for parameter, t in get_type_hints(cls).items():
            if __is_primitive(t):
                constructor_args[parameter] = d[parameter]
            else:
                constructor_args[parameter] = t.from_json(d[parameter])
        return cls(**constructor_args)

    def __from_path(path):
        with open(path, "r") as f:
            return __from_json(json.load(f))

    cls.from_json = __from_json
    cls.from_path = __from_path
    return cls


def tojson(cls):
    def __to_json(self):
        dict_representation = {}
        for parameter, t in get_type_hints(self).items():
            if __is_primitive(t):
                dict_representation[parameter] = self.__getattribute__(parameter)
            else:
                dict_representation[parameter] = self.__getattribute__(
                    parameter
                ).to_json()
        return dict_representation

    cls.to_json = __to_json
    return cls
