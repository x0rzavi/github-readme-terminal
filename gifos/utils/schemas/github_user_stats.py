from dataclasses import dataclass

from gifos.utils.schemas.github_user_rank import GithubUserRank


@dataclass
class GithubUserStats:
    """A class to represent a GitHub user's statistics.

    This class represents a GitHub user's statistics.

    Attributes:
        account_name: A string that represents the user's account name.
        total_followers: An integer that represents the total number of followers the user has.
        total_stargazers: An integer that represents the total number of stargazers the user has.
        total_issues: An integer that represents the total number of issues the user has opened.
        total_commits_all_time: An integer that represents the total number of commits the user has made all time.
        total_commits_last_year: An integer that represents the total number of commits the user has made in the last year.
        total_pull_requests_made: An integer that represents the total number of pull requests the user has made.
        total_pull_requests_merged: An integer that represents the total number of the user's pull requests that have been merged.
        pull_requests_merge_percentage: A float that represents the percentage of the user's pull requests that have been merged.
        total_pull_requests_reviewed: An integer that represents the total number of pull requests the user has reviewed.
        total_repo_contributions: An integer that represents the total number of repositories the user has contributed to.
        languages_sorted: A list of tuples that represents the user's most used languages, sorted by usage. Each tuple contains a language name and a usage percentage.
        user_rank: A `GithubUserRank` object that represents the user's GitHub rank.
    """

    __slots__ = [
        "account_name",
        "total_followers",
        "total_stargazers",
        "total_issues",
        "total_commits_all_time",
        "total_commits_last_year",
        "total_pull_requests_made",
        "total_pull_requests_merged",
        "pull_requests_merge_percentage",
        "total_pull_requests_reviewed",
        "total_repo_contributions",
        "languages_sorted",
        "user_rank",
    ]
    account_name: str
    total_followers: int
    total_stargazers: int
    total_issues: int
    total_commits_all_time: int
    total_commits_last_year: int
    total_pull_requests_made: int
    total_pull_requests_merged: int
    pull_requests_merge_percentage: float
    total_pull_requests_reviewed: int
    total_repo_contributions: int
    languages_sorted: list
    user_rank: GithubUserRank
