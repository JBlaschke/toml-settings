from curses.ascii import SP
from typing  import Any, Union, Type, List
from pathlib import Path

import msgspec
from msgspec import Struct

from .error       import FaultySpec
from .parsers     import Parser
from .environment import Getter


class Setting(Struct):
    attribute: str
    key: str
    parser: Parser
    default: Union[bool, int, float, str, List, None]
    doc: str
    environ: str = ""
    environ_getter: Union[Getter, None] = None

    def validate(self):
        # Cast parser to Parser type (if necessary)
        if not isinstance(self.parser, Parser):
            self.parser = Parser(self.parser)
        # Cast getter to Getter type
        if self.environ_getter is not None:
            if not isinstance(self.environ_getter, Getter):
                self.environ_getter = Getter(self.environ_getter)

        # Run the default through its own parser
        self.default = self.parser(self.default)

        return True


class Section(Struct):
    name: str
    settings: List[Setting] = list()

    def add(self, setting):
        self.settings.append(setting)
        return self

    def validate(self):
        for s in self.settings:
            if not s.validate():
                return False
        return True

    def __iter__(self):
        return self.settings.__iter__()

    def __getitem__(self, idx):
        return self.settings[idx]


class Spec(Struct):
    sections: List[Section] = list()

    def add(self, section):
        if not section.validate():
            raise FaultySpec([s for s in section.invalid()])
        self.sections.append(section)
        return self

    def validate(self):
        for s in self.sections:
            if not s.validate():
                return False
        return True

    def __iter__(self):
        return self.sections.__iter__()

    def __getitem__(self, idx):
        return self.sections[idx]


def enc_hook(obj: Any) -> Any:
    if isinstance(obj, Parser):
        # convert the Parser to a str
        return str(obj)
    elif isinstance(obj, Getter):
        # convert the Getter to a str
        return str(obj)
    elif isinstance(obj, Path):
        return str(obj)
    else:
        # Raise a TypeError for other types
        raise TypeError(f"Objects of type {type(obj)} are not supported")


def dec_hook(type: Type, obj: Any) -> Any:
    # `type` here is the value of the custom type annotation being decoded.
    if type is Parser:
        # Convert ``obj`` (which should be a ``str``) to the corresponding
        # Parser type (which loads the parser function named in `obj`)
        return Parser(obj)
    elif type is Getter:
        # Convert ``obj`` (which should be a ``str``) to the corresponding
        # Getter type (which loads the parser function named in `obj`)
        return Getter(obj)
    elif type is Path:
        return Path(obj)
    else:
        # Raise a TypeError for other types
        raise TypeError(f"Objects of type {type} are not supported")


ENC         = msgspec.json.Encoder(enc_hook=enc_hook)
SETTING_DEC = msgspec.json.Decoder(Setting, dec_hook=dec_hook)
SECTION_DEC = msgspec.json.Decoder(Section, dec_hook=dec_hook)
SPEC_DEC    = msgspec.json.Decoder(Spec, dec_hook=dec_hook)


def to_json(spec):
    return ENC.encode(spec)


def from_json(spec_json):
    return SPEC_DEC.decode(spec_json).validate()