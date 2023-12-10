"""
Reference: https://github.com/anuraghazra/github-readme-stats/blob/23472f40e81170ba452c38a99abc674db0000ce6/src/calculateRank.js
"""


def exponentialCdf(x):
    return 1 - 2**-x


def logNormalCdf(x):
    return x / (1 + x)


def calcRank(
    allCommits: bool,
    commits: int,
    prs: int,
    issues: int,
    reviews: int,
    stars: int,
    followers: int,
) -> dict:
    COMMITS_MEDIAN = 1000 if allCommits else 250
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
            COMMITS_WEIGHT * exponentialCdf(commits / COMMITS_MEDIAN)
            + PRS_WEIGHT * exponentialCdf(prs / PRS_MEDIAN)
            + ISSUES_WEIGHT * exponentialCdf(issues / ISSUES_MEDIAN)
            + REVIEWS_WEIGHT * exponentialCdf(reviews / REVIEWS_MEDIAN)
            + STARS_WEIGHT * logNormalCdf(stars / STARS_MEDIAN)
            + FOLLOWERS_WEIGHT * logNormalCdf(followers / FOLLOWERS_MEDIAN)
        )
        / TOTAL_WEIGHT
    )

    level = LEVELS[
        next((i for i, t in enumerate(THRESHOLDS) if rank * 100 <= t), len(LEVELS) - 1)
    ]
    return {"level": level, "percentile": round(rank * 100, 2)}
