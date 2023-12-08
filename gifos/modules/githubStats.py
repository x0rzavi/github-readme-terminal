# TODO
# [x] Language list
# [x] Rank
# [] Optimize API calls
# [] Catch errors
# [] Count total commits from all time
# [] Retry on error
# [] Ignore repo
from icecream import ic
from dotenv import load_dotenv
import os
import requests
from .calcRank import calcRank

load_dotenv()
githubToken = os.getenv("GITHUB_TOKEN")
endPoint = "https://api.github.com/graphql"
headers = {"Authorization": f"bearer {githubToken}"}


def fetchRepoStats(username: str, repoEndCursor: str = None) -> dict:
    query = """
    query repoInfo(
        $username: String!
        $repoEndCursor: String
    ) {
        user(login: $username) {
            repositories (
                first: 100,
                after: $repoEndCursor
                orderBy: { field: STARGAZERS, direction: DESC }
                ownerAffiliations: OWNER
            ) {
                totalCount
                nodes {
                    isFork
                    stargazerCount
                    languages(
                    first: 10
                    orderBy: { field: SIZE, direction: DESC }
                    ) {
                        edges {
                            node {
                                name
                                color
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
        rateLimit {
            cost
            limit
            remaining
            used
            resetAt
        }
    }
    """
    variables = {"username": username, "repoEndCursor": repoEndCursor}

    response = requests.post(
        endPoint, json={"query": query, "variables": variables}, headers=headers
    )

    if response.status_code == 200:
        jsonObj = response.json()
        if "errors" in jsonObj:
            ic("Error!", jsonObj["errors"])
        else:
            return jsonObj["data"]["user"]["repositories"]
    else:
        ic("Error!", response.status_code)


def fetchUserStats(username: str) -> dict:
    query = """
    query userInfo($username: String!) {
        user(login: $username) {
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
        rateLimit {
            cost
            limit
            remaining
            used
            resetAt
        }
    }
    """
    variables = {"username": username}

    response = requests.post(
        endPoint, json={"query": query, "variables": variables}, headers=headers
    )

    if response.status_code == 200:
        jsonObj = response.json()
        if "errors" in jsonObj:
            ic("Error!", jsonObj["errors"])
        else:
            return jsonObj["data"]["user"]
    else:
        ic("Error!", response.status_code)


def calcUserStats(username: str) -> dict:
    repoEndCursor = None
    totalStargazers = 0
    languagesDict = {}

    while True:  # paginate repository stats
        repoStats = fetchRepoStats(username, repoEndCursor)
        if repoStats:
            repos = repoStats["nodes"]
            for repo in repos:
                totalStargazers += repo["stargazerCount"]
                if not repo["isFork"]:
                    languages = repo["languages"]["edges"]
                    for language in languages:
                        if language["node"]["name"] in languagesDict:
                            languagesDict[language["node"]["name"]] += language["size"]
                        else:
                            languagesDict[language["node"]["name"]] = language["size"]
            if repoStats["pageInfo"]["hasNextPage"]:
                repoEndCursor = repoStats["pageInfo"]["endCursor"]
            else:
                break
        else:
            break

    totalLanguagesSize = sum([size for _, size in languagesDict.items()])
    languagesPercentage = {
        language: round((size / totalLanguagesSize) * 100, 2)
        for language, size in languagesDict.items()
    }
    languagesSorted = sorted(
        languagesPercentage.items(), key=lambda n: n[1], reverse=True
    )

    userStats = fetchUserStats(username)
    userDetails = {}
    userDetails["accountName"] = userStats["name"]
    userDetails["totalFollowers"] = userStats["followers"]["totalCount"]
    userDetails["totalStargazers"] = totalStargazers
    userDetails["totalCommitsLastYear"] = (
        userStats["contributionsCollection"]["restrictedContributionsCount"]
        + userStats["contributionsCollection"]["totalCommitContributions"]
    )
    userDetails["totalPullRequestsMade"] = userStats["pullRequests"]["totalCount"]
    userDetails["totalPullRequestsMerged"] = userStats["mergedPullRequests"][
        "totalCount"
    ]
    userDetails["pullRequestsMergePercentage"] = round(
        (userDetails["totalPullRequestsMerged"] / userDetails["totalPullRequestsMade"])
        * 100,
        2,
    )
    userDetails["totalPullRequestsReviewed"] = userStats["contributionsCollection"][
        "totalPullRequestReviewContributions"
    ]
    userDetails["totalIssues"] = userStats["issues"]["totalCount"]
    userDetails["totalRepoContributions"] = userStats["repositoriesContributedTo"][
        "totalCount"
    ]
    userDetails["languagesSorted"] = languagesSorted[:6]  # top 6 languages
    userDetails["userRank"] = calcRank(
        False,
        userDetails["totalCommitsLastYear"],
        userDetails["totalPullRequestsMade"],
        userDetails["totalIssues"],
        userDetails["totalPullRequestsReviewed"],
        userDetails["totalStargazers"],
        userDetails["totalFollowers"],
    )

    return userDetails
