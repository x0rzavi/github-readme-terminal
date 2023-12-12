from dataclasses import dataclass


@dataclass
class githubUserRank:
    __slots__ = ["level", "percentile"]
    level: str
    percentile: float
