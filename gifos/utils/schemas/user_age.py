from dataclasses import dataclass


@dataclass
class UserAge:
    __slots__ = ["years", "months", "days"]
    years: int
    months: int
    days: int
