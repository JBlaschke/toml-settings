class MalformedSettingsException(Exception):
    """
    Raise this error whenever settings inputs don't follow the format: `a.b = c`
    """


class NotAVector(Exception):
    """
    Raise this error whenever trying to parse a vector representation that is
    malformed in any way.
    """


class FaultySpec(Exception):
    """
    Raise this error whenever there is faulty Setting in Spec
    """
    def __init__(self, message):
        super().__init__(message)


class UnknownParser(Exception):
    """
    Raise this error whenever there is an unknown parser in the Parser container
    """
    def __init__(self, message):
        super().__init__(message)


class UnknownGetter(Exception):
    """
    Raise this error whenever there is an unknown parser in the Getter container
    """
    def __init__(self, message):
        super().__init__(message)