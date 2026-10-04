import requests
import json


def get_repositories(user_id):
    url = "https://api.github.com/users/" + user_id + "/repos"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    repositories = json.loads(response.text)

    results = []

    for repo in repositories:
        repo_name = repo["name"]

        commit_url = "https://api.github.com/repos/" + user_id + "/" + repo_name + "/commits"

        commit_response = requests.get(commit_url)

        if commit_response.status_code == 200:
            commits = json.loads(commit_response.text)
            results.append((repo_name, len(commits)))

    return results


if __name__ == "__main__":
    user_id = input("Enter GitHub username: ")

    repositories = get_repositories(user_id)

    for repo in repositories:
        print("Repo:", repo[0], "Number of commits:", repo[1])
