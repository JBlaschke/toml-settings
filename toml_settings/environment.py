from os          import environ
from pathlib     import Path
from collections import namedtuple

from .parsers import str2bool
from .error   import UnknownGetter


def get_str(x):
    """
    Return string representation of the environment variable `x`
    """
    return environ[x]


def get_path(x):
    """
    Return string representation of the environment variable `x`
    """
    return Path(environ[x])


def get_bool(x):
    """
    Return boolean representation of the environment variable `x`
    """
    return str2bool(environ[x].strip())


def get_int(x):
    """
    Return integer representation of the environment variable `x`
    """
    return int(environ[x])


class Getter:
    Assoc = namedtuple("Assoc", ["func", "str"])
    funcs = [get_str, get_path, get_bool, get_int]
    # Populate getter <-> string associations
    _assoc = list()
    for f in funcs:
        _assoc.append(Assoc(f, f.__name__))

    def __init__(self, parser):
        if isinstance(parser, str):
            matched = False
            for a in self._assoc:
                if a.str == parser:
                    self._parser = a.func
                    matched = True
                    break
            if not matched:
                raise UnknownGetter(
                    f"Cannot de-stringify parser={parser}"
                )
        else:
            self._parser = parser

    def __call__(self, *args, **kwargs):
        return self._parser(*args, **kwargs)

    def __repr__(self):
        return self._parser.__name__

    def __eq__(self, other):
        return self._parser.__name__ == other._parser.__name__