from dataclasses import dataclass


@dataclass
class ansiEscape:
    __slots__ = ["data", "oper"]
    data: str
    oper: str
