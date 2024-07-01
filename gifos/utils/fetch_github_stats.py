# TODO
# [] Language colors
# [] Profile image ascii art
# [] Optimize code
# [] Optimize API calls
# [] Catch errors
# [] Retry on error

import os
import requests
import sys

from dotenv import load_dotenv

from gifos.utils.calc_github_rank import calc_github_rank
from gifos.utils.schemas.github_user_stats import GithubUserStats

"""This module contains a function for fetching a GitHub user's statistics."""

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GRAPHQL_ENDPOINT = "https://api.github.com/graphql"


def fetch_repo_stats(user_name: str, repo_end_cursor: str = None) -> dict:
    """Fetch statistics for a user's repositories.

    This function sends a GraphQL query to the GitHub API to fetch statistics for a
    user's repositories. The function uses the `GITHUB_TOKEN` environment variable for
    authentication and the `GRAPHQL_ENDPOINT` constant for the API endpoint.

    :param user_name: The username of the user to fetch statistics for.
    :type user_name: str
    :param repo_end_cursor: The end cursor for pagination. If not provided, the function
        fetches statistics from the beginning.
    :type repo_end_cursor: str, optional
    :return: A dictionary containing the fetched statistics if the request is
        successful, otherwise None.
    :rtype: dict or None
    """
    query = """
    query repoInfo(
        $user_name: String!
        $repo_end_cursor: String
    ) {
        user(login: $user_name) {
            repositories (
                first: 100,
                after: $repo_end_cursor
                orderBy: { field: STARGAZERS, direction: DESC }
                ownerAffiliations: OWNER
            ) {
                totalCount
                nodes {
                    name
                    isFork
                    stargazerCount
                    languages(
                    first: 10
                    orderBy: { field: SIZE, direction: DESC }
                    ) {
                        edges {
                            node {
                                name
                                # color
                            }
                            size
                        }
                    }
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
        # rateLimit {
        #     cost
        #     limit
        #     remaining
        #     used
        #     resetAt
        # }
    }
    """
    headers = {"Authorization": f"bearer {GITHUB_TOKEN}"}
    variables = {"user_name": user_name, "repo_end_cursor": repo_end_cursor}

    response = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": query, "variables": variables},
        headers=headers,
    )

    if response.status_code == 200:
        json_obj = response.json()
        if "errors" in json_obj:
            print(f"ERROR: {json_obj['errors']}")
            return None
        else:
            print(f"INFO: Repository details fetched for {user_name}")
            return json_obj["data"]["user"]["repositories"]
    else:
        print(f"ERROR: {response.status_code}")
        return None


def fetch_user_stats(user_name: str) -> dict:
    """Fetch statistics for a GitHub user.

    This function sends a GraphQL query to the GitHub API to fetch statistics for a
    GitHub user. The function uses the `GITHUB_TOKEN` environment variable for
    authentication and the `GRAPHQL_ENDPOINT` constant for the API endpoint.

    :param user_name: The username of the user to fetch statistics for.
    :type user_name: str
    :return: A dictionary containing the fetched statistics if the request is
        successful, otherwise None.
    :rtype: dict or None
    """
    query = """
    query userInfo($user_name: String!) {
        user(login: $user_name) {
            name
            followers (first: 1) {
                totalCount
            }
            repositoriesContributedTo (
                first: 1
                contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]
            ) {
                totalCount
            }
            contributionsCollection {
                # contributionCalendar {
                #     totalContributions
                # }
                totalCommitContributions
                restrictedContributionsCount
                totalPullRequestReviewContributions
            }
            issues(first: 1) {
                totalCount
            }
            pullRequests(first: 1) {
                totalCount
            }
            mergedPullRequests: pullRequests(states: MERGED, first: 1) {
                totalCount
            }
        }
        # rateLimit {
        #     cost
        #     limit
        #     remaining
        #     used
        #     resetAt
        # }
    }
    """

    headers = {"Authorization": f"bearer {GITHUB_TOKEN}"}
    variables = {"user_name": user_name}

    response = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": query, "variables": variables},
        headers=headers,
    )

    if response.status_code == 200:
        json_obj = response.json()
        if "errors" in json_obj:
            print(f"ERROR: {json_obj['errors']}")
            return None
        else:
            print(f"INFO: User details fetched for {user_name}")
            return json_obj["data"]["user"]
    else:
        print(f"ERROR: {response.status_code}")
        return None


# Reference: https://github.com/anuraghazra/github-readme-stats/blob/23472f40e81170ba452c38a99abc674db0000ce6/src/fetchers/stats-fetcher.js#L170
def fetch_total_commits(user_name: str) -> int:
    """Fetch the total number of commits (lifetime) made by a GitHub user.

    This function sends a GET request to the GitHub REST API to fetch the total number
    of commits made by a GitHub user. The function uses the `GITHUB_TOKEN` environment
    variable for authentication.

    :param user_name: The username of the user to fetch the total number of commits for.
    :type user_name: str
    :return: The total number of commits made by the user if the request is successful,
        otherwise None.
    :rtype: int or None
    """
    REST_API_URL = f"https://api.github.com/search/commits?q=author:{user_name}"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "x0rzavi",
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {GITHUB_TOKEN}",
    }
    response = requests.get(REST_API_URL, headers=headers)
    if response.status_code == 200:
        json_obj = response.json()
        total_commits_all_time = json_obj["total_count"]
        print(f"INFO: Total commits fetched for {user_name}")
        return total_commits_all_time
    else:
        print(f"ERROR: {response.status_code}")
        return None


def fetch_github_stats(
    user_name: str, ignore_repos: list = None, include_all_commits: bool = False
) -> GithubUserStats:
    """Fetch GitHub statistics for a user.

    This function fetches various statistics for a GitHub user. The function uses the
    `GITHUB_TOKEN` environment variable for authentication.

    :param user_name: The username of the user to fetch statistics for.
    :type user_name: str
    :param ignore_repos: A list of repository names to ignore when fetching statistics.
        If not provided, all repositories are included.
    :type ignore_repos: list, optional
    :param include_all_commits: A boolean indicating whether to include all commits when
        calculating the user's GitHub rank. If False, only commits from the last year
        are included.
    :type include_all_commits: bool, optional
    :return: A `GithubUserStats` object containing the fetched statistics if the request
        is successful, otherwise None.
    :rtype: GithubUserStats or None
    """
    if not GITHUB_TOKEN:
        print("ERROR: Please provide GITHUB_TOKEN")
        sys.exit(1)

    repo_end_cursor = None
    total_stargazers = 0
    languages_dict = {}

    def update_languages(languages, languages_dict):
        for language in languages:
            language_name = language["node"]["name"]
            language_size = language["size"]
            languages_dict[language_name] = (
                languages_dict.get(language_name, 0) + language_size
            )

    def process_repo(repos, ignore_repos, languages_dict):
        total_stargazers = 0
        for repo in repos:
            if repo["name"] not in (ignore_repos or []):
                total_stargazers += repo["stargazerCount"]
                if not repo["isFork"]:
                    update_languages(repo["languages"]["edges"], languages_dict)
        return total_stargazers

    while True:  # paginate repository stats
        repo_stats = fetch_repo_stats(user_name, repo_end_cursor)
        if repo_stats:
            total_stargazers = process_repo(
                repo_stats["nodes"], ignore_repos, languages_dict
            )
            if repo_stats["pageInfo"]["hasNextPage"]:
                repo_end_cursor = repo_stats["pageInfo"]["endCursor"]
            else:
                break
        else:
            break

    total_commits_all_time = fetch_total_commits(user_name)  # fetch only once
    total_languages_size = sum(languages_dict.values())
    languages_percentage = {
        language: round((size / total_languages_size) * 100, 2)
        for language, size in languages_dict.items()
    }
    languages_sorted = sorted(
        languages_percentage.items(), key=lambda n: n[1], reverse=True
    )

    user_stats = fetch_user_stats(user_name)

    if user_stats:
        if user_stats["pullRequests"]["totalCount"] > 0:
            pull_requests_merge_percentage = round(
                (
                    user_stats["mergedPullRequests"]["totalCount"]
                    / user_stats["pullRequests"]["totalCount"]
                )
                * 100,
                2,
            )
        else:
            pull_requests_merge_percentage = 0

        user_details = GithubUserStats(
            account_name=user_stats["name"],
            total_followers=user_stats["followers"]["totalCount"],
            total_stargazers=total_stargazers,
            total_issues=user_stats["issues"]["totalCount"],
            total_commits_all_time=total_commits_all_time,
            total_commits_last_year=(
                user_stats["contributionsCollection"]["restrictedContributionsCount"]
                + user_stats["contributionsCollection"]["totalCommitContributions"]
            ),
            total_pull_requests_made=user_stats["pullRequests"]["totalCount"],
            total_pull_requests_merged=user_stats["mergedPullRequests"]["totalCount"],
            pull_requests_merge_percentage=pull_requests_merge_percentage,
            total_pull_requests_reviewed=user_stats["contributionsCollection"][
                "totalPullRequestReviewContributions"
            ],
            total_repo_contributions=user_stats["repositoriesContributedTo"][
                "totalCount"
            ],
            languages_sorted=languages_sorted[:6],  # top 6 languages
            user_rank=calc_github_rank(
                include_all_commits,
                total_commits_all_time
                if include_all_commits
                else (
                    user_stats["contributionsCollection"][
                        "restrictedContributionsCount"
                    ]
                    + user_stats["contributionsCollection"]["totalCommitContributions"]
                ),
                user_stats["pullRequests"]["totalCount"],
                user_stats["issues"]["totalCount"],
                user_stats["contributionsCollection"][
                    "totalPullRequestReviewContributions"
                ],
                total_stargazers,
                user_stats["followers"]["totalCount"],
            ),
        )
        return user_details
    else:
        return None
