from dataclasses import dataclass


@dataclass
class AnsiEscape:
    __slots__ = ["data", "oper"]
    data: str
    oper: str
