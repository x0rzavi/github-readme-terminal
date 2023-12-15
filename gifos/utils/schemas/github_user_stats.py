from dataclasses import dataclass

from gifos.utils.schemas.github_user_rank import GithubUserRank


@dataclass
class GithubUserStats:
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
