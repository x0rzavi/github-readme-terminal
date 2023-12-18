from dataclasses import dataclass


@dataclass
class AnsiEscape:
    """A class to represent an ANSI escape sequence.

    This class represents an ANSI escape sequence, which is used to control the
    formatting, color, and other output options on text terminals. The class has two
    attributes: `data` and `oper`.

    Attributes:     data: A string that represents the data of the escape sequence.
    oper: A string that represents the operation of the escape sequence.
    """

    __slots__ = ["data", "oper"]
    data: str
    oper: str
