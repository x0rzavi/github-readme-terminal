from dataclasses import dataclass
from .githubUserRank import githubUserRank


@dataclass
class githubUserStats:
    __slots__ = [
        "accountName",
        "totalFollowers",
        "totalStargazers",
        "totalIssues",
        "totalCommitsAllTime",
        "totalCommitsLastYear",
        "totalPullRequestsMade",
        "totalPullRequestsMerged",
        "pullRequestsMergePercentage",
        "totalPullRequestsReviewed",
        "totalRepoContributions",
        "languagesSorted",
        "userRank"
    ]
    accountName: str
    totalFollowers: int
    totalStargazers: int
    totalIssues: int
    totalCommitsAllTime: int
    totalCommitsLastYear: int
    totalPullRequestsMade: int
    totalPullRequestsMerged: int
    pullRequestsMergePercentage: float
    totalPullRequestsReviewed: int
    totalRepoContributions: int
    languagesSorted: list
    userRank: githubUserRank
