from dataclasses import dataclass


@dataclass
class ansiEscape:
    __slots__ = ["data", "op"]
    data: str
    op: str
