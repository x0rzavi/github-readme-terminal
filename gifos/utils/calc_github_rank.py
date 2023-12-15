# Reference: https://github.com/anuraghazra/github-readme-stats/blob/23472f40e81170ba452c38a99abc674db0000ce6/src/calculateRank.js
from gifos.utils.schemas.github_user_rank import GithubUserRank


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
