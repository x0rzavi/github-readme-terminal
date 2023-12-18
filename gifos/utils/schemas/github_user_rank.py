from dataclasses import dataclass


@dataclass
class GithubUserRank:
    """A class to represent a GitHub user's rank.

    This class represents a GitHub user's rank, which is calculated based on their
    statistics. The class has two attributes: `level` and `percentile`.

    Attributes:     level: A string that represents the user's rank level.
    percentile: A float that represents the user's percentile rank.
    """
    __slots__ = ["level", "percentile"]
    level: str
    percentile: float
