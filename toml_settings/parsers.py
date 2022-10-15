from collections import namedtuple
from pathlib     import Path

from .error import NotAVector, UnknownParser


def str2bool(x):
    """
    Parse a string representation of a boolean
    """
    yes = {"1", "on", "true"}
    return x.lower() in yes


def parse_bool(x):
    """
    Parse string, integer, or boolean representation of a boolean
    """
    # Toml already parses some inputs, so the input might already have the
    # correct format
    if isinstance(x, bool):
        return x

    if isinstance(x, str):
        return str2bool(x)

    return bool(x)


def parse_strvec(x, elt_parser):
    """
    Parse a string representation of a vector. All elements use the same parser
    `elt_parser`. The element parser is only invoked if `x` is a well-formed
    string representation of a vecotr. Vector elements are delimited by commas.
    """
    # Toml already parses some inputs, so the input might already have the
    # correct format
    if isinstance(x, list):
        return tuple(x)

    if isinstance(x, tuple):
        return x

    if not isinstance(x, str):
        raise NotAVector

    if x[0] != "[":
        raise NotAVector

    if x[-1] != "]":
        raise NotAVector

    if x.count("[") != 1:
        raise NotAVector

    if x.count("]") != 1:
        raise NotAVector

    return tuple(
        [elt_parser(y.strip()) for y in x[1:-1].split(",") if len(y) > 0]
    )


def parse_strvec_bool(x):
    """
    Narrowing of parse_strvec:
    parse_strvec_int = parse_strvec(___, parse_bool)
    """
    return parse_strvec(x, parse_bool)


def parse_strvec_int(x):
    """
    Narrowing of parse_strvec:
    parse_strvec_int = parse_strvec(___, int)
    """
    return parse_strvec(x, int)


def parse_strvec_float(x):
    """
    Narrowing of parse_strvec:
    parse_strvec_int = parse_strvec(___, float)
    """
    return parse_strvec(x, float)


def parse_strvec_str(x):
    """
    Narrowing of parse_strvec:
    parse_strvec_int = parse_strvec(___, str)
    """
    return parse_strvec(x, str)


class Parser:
    Assoc = namedtuple("Assoc", ["func", "str"])
    funcs = [
        parse_bool, int, float, str, Path,
        parse_strvec_bool, parse_strvec_int, parse_strvec_float, parse_strvec_str
    ]
    # Populate parser <-> string associations
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
                raise UnknownParser(
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