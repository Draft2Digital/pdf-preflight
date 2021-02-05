from collections import namedtuple, Mapping


def namedtuple_with_defaults(typename, field_names, default_values=()):
    # From http://stackoverflow.com/questions/11351032/named-tuple-and-optional-keyword-arguments
    T = namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T


Issue = namedtuple_with_defaults(
    "Issue",
    ["page", "rule", "desc", "fixable"],
    default_values={
        "page": None,
        "rule": None,
        "desc": None,
        "fixable": False
    }
)
