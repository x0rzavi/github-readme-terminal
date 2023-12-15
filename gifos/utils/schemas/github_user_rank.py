from dataclasses import dataclass


@dataclass
class GithubUserRank:
    __slots__ = ["level", "percentile"]
    level: str
    percentile: float
