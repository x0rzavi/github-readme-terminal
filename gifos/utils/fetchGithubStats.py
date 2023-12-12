# TODO
# [] Language colors
# [] Profile image ascii art
# [] Optimize code
# [] Optimize API calls
# [] Catch errors
# [] Retry on error

import os
import requests
from dotenv import load_dotenv
from .calcGithubRank import calcGithubRank
from .schemas.githubUserStats import githubUserStats

load_dotenv()
githubToken = os.getenv("GITHUB_TOKEN")


def fetchRepoStats(userName: str, repoEndCursor: str = None) -> dict:
    query = """
    query repoInfo(
        $userName: String!
        $repoEndCursor: String
    ) {
        user(login: $userName) {
            repositories (
                first: 100,
                after: $repoEndCursor
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
    endPoint = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {githubToken}"}
    variables = {"userName": userName, "repoEndCursor": repoEndCursor}

    response = requests.post(
        endPoint, json={"query": query, "variables": variables}, headers=headers
    )

    if response.status_code == 200:
        jsonObj = response.json()
        if "errors" in jsonObj:
            print(f"ERROR: {jsonObj['errors']}")
            return
        else:
            print(f"INFO: Repository details fetched for {userName}")
            return jsonObj["data"]["user"]["repositories"]
    else:
        print(f"ERROR: {response.status_code}")
        return


def fetchUserStats(userName: str) -> dict:
    query = """
    query userInfo($userName: String!) {
        user(login: $userName) {
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
    endPoint = "https://api.github.com/graphql"
    headers = {"Authorization": f"bearer {githubToken}"}
    variables = {"userName": userName}

    response = requests.post(
        endPoint, json={"query": query, "variables": variables}, headers=headers
    )

    if response.status_code == 200:
        jsonObj = response.json()
        if "errors" in jsonObj:
            print(f"ERROR: {jsonObj['errors']}")
            return
        else:
            print(f"INFO: User details fetched for {userName}")
            return jsonObj["data"]["user"]
    else:
        print(f"ERROR: {response.status_code}")
        return


"""
Reference: https://github.com/anuraghazra/github-readme-stats/blob/23472f40e81170ba452c38a99abc674db0000ce6/src/fetchers/stats-fetcher.js#L170
"""


def fetchTotalCommits(userName: str) -> int:
    url = f"https://api.github.com/search/commits?q=author:{userName}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.cloak-preview",
        "Authorization": f"token {githubToken}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        jsonObj = response.json()
        totalCommitsAllTime = jsonObj["total_count"]
        print(f"INFO: Total commits fetched for {userName}")
        return totalCommitsAllTime
    else:
        print(f"ERROR: {response.status_code}")
        return


def fetchGithubStats(
    userName: str, ignoreRepos: list = None, includeAllCommits: bool = False
) -> githubUserStats:
    repoEndCursor = None
    totalStargazers = 0
    languagesDict = {}

    def updateLanguages(languages, languagesDict):
        for language in languages:
            languageName = language["node"]["name"]
            languageSize = language["size"]
            languagesDict[languageName] = (
                languagesDict.get(languageName, 0) + languageSize
            )

    def processRepo(repos, ignoreRepos, languagesDict):
        totalStargazers = 0
        for repo in repos:
            if repo["name"] not in (ignoreRepos or []):
                totalStargazers += repo["stargazerCount"]
                if not repo["isFork"]:
                    updateLanguages(repo["languages"]["edges"], languagesDict)
        return totalStargazers

    while True:  # paginate repository stats
        repoStats = fetchRepoStats(userName, repoEndCursor)
        if repoStats:
            totalStargazers = processRepo(
                repoStats["nodes"], ignoreRepos, languagesDict
            )
            if repoStats["pageInfo"]["hasNextPage"]:
                repoEndCursor = repoStats["pageInfo"]["endCursor"]
            else:
                break
        else:
            break

    totalLanguagesSize = sum(languagesDict.values())
    languagesPercentage = {
        language: round((size / totalLanguagesSize) * 100, 2)
        for language, size in languagesDict.items()
    }
    languagesSorted = sorted(
        languagesPercentage.items(), key=lambda n: n[1], reverse=True
    )

    userStats = fetchUserStats(userName)
    if userStats:
        userDetails = githubUserStats(
            accountName=userStats["name"],
            totalFollowers=userStats["followers"]["totalCount"],
            totalStargazers=totalStargazers,
            totalIssues=userStats["issues"]["totalCount"],
            totalCommitsAllTime=fetchTotalCommits(userName),
            totalCommitsLastYear=(
                userStats["contributionsCollection"]["restrictedContributionsCount"]
                + userStats["contributionsCollection"]["totalCommitContributions"]
            ),
            totalPullRequestsMade=userStats["pullRequests"]["totalCount"],
            totalPullRequestsMerged=userStats["mergedPullRequests"]["totalCount"],
            pullRequestsMergePercentage=round(
                (
                    userStats["mergedPullRequests"]["totalCount"]
                    / userStats["pullRequests"]["totalCount"]
                )
                * 100,
                2,
            ),
            totalPullRequestsReviewed=userStats["contributionsCollection"][
                "totalPullRequestReviewContributions"
            ],
            totalRepoContributions=userStats["repositoriesContributedTo"]["totalCount"],
            languagesSorted=languagesSorted[:6],  # top 6 languages
            userRank=calcGithubRank(
                includeAllCommits,
                fetchTotalCommits(userName)
                if includeAllCommits
                else (
                    userStats["contributionsCollection"]["restrictedContributionsCount"]
                    + userStats["contributionsCollection"]["totalCommitContributions"]
                ),
                userStats["pullRequests"]["totalCount"],
                userStats["issues"]["totalCount"],
                userStats["contributionsCollection"][
                    "totalPullRequestReviewContributions"
                ],
                totalStargazers,
                userStats["followers"]["totalCount"],
            ),
        )

        return userDetails
