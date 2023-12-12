from dataclasses import dataclass


@dataclass
class userAge:
    __slots__ = ["years", "months", "days"]
    years: int
    months: int
    days: int
