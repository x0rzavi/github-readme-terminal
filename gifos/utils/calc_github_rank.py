# Reference: https://github.com/anuraghazra/github-readme-stats/blob/23472f40e81170ba452c38a99abc674db0000ce6/src/calculateRank.js
from gifos.utils.schemas.github_user_rank import GithubUserRank

"""This module contains a utility function for calculating a GitHub user's rank."""

def exponential_cdf(x):
    return 1 - 2**-x


def log_normal_cdf(x):
    return x / (1 + x)


def calc_github_rank(
    all_commits: bool,
    commits: int,
    prs: int,
    issues: int,
    reviews: int,
    stars: int,
    followers: int,
) -> GithubUserRank:
    """Calculate the GitHub rank of a user based on their activity.

    The rank is calculated using a weighted sum of various activity metrics, including
    commits, pull requests, issues, reviews, stars, and followers. Each metric is
    normalized using a cumulative distribution function (either exponential or log-
    normal) before being weighted and summed.

    :param all_commits: Whether to consider all commits or only those in the last year.
    :type all_commits: bool
    :param commits: The number of commits the user has made.
    :type commits: int
    :param prs: The number of pull requests the user has made.
    :type prs: int
    :param issues: The number of issues the user has opened.
    :type issues: int
    :param reviews: The number of reviews the user has made.
    :type reviews: int
    :param stars: The number of stars the user's repositories have received.
    :type stars: int
    :param followers: The number of followers the user has.
    :type followers: int
    :return: The user's GitHub rank and percentile.
    :rtype: GithubUserRank
    """
    COMMITS_MEDIAN = 1000 if all_commits else 250
    COMMITS_WEIGHT = 2
    PRS_MEDIAN = 50
    PRS_WEIGHT = 3
    ISSUES_MEDIAN = 25
    ISSUES_WEIGHT = 1
    REVIEWS_MEDIAN = 2
    REVIEWS_WEIGHT = 1
    STARS_MEDIAN = 50
    STARS_WEIGHT = 4
    FOLLOWERS_MEDIAN = 10
    FOLLOWERS_WEIGHT = 1
    TOTAL_WEIGHT = (
        COMMITS_WEIGHT
        + PRS_WEIGHT
        + ISSUES_WEIGHT
        + REVIEWS_WEIGHT
        + STARS_WEIGHT
        + FOLLOWERS_WEIGHT
    )

    THRESHOLDS = [1, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100]
    LEVELS = ["S", "A+", "A", "A-", "B+", "B", "B-", "C+", "C"]
    rank = (
        1
        - (
            COMMITS_WEIGHT * exponential_cdf(commits / COMMITS_MEDIAN)
            + PRS_WEIGHT * exponential_cdf(prs / PRS_MEDIAN)
            + ISSUES_WEIGHT * exponential_cdf(issues / ISSUES_MEDIAN)
            + REVIEWS_WEIGHT * exponential_cdf(reviews / REVIEWS_MEDIAN)
            + STARS_WEIGHT * log_normal_cdf(stars / STARS_MEDIAN)
            + FOLLOWERS_WEIGHT * log_normal_cdf(followers / FOLLOWERS_MEDIAN)
        )
        / TOTAL_WEIGHT
    )

    level = LEVELS[
        next((i for i, t in enumerate(THRESHOLDS) if rank * 100 <= t), len(LEVELS) - 1)
    ]
    percentile = round(rank * 100, 2)
    return GithubUserRank(level, percentile)
