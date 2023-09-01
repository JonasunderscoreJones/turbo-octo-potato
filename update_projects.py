import os
import json
import requests
from datetime import datetime

# GitHub API base URL
BASE_URL = "https://api.github.com/repos/"

# Function to get the default branch name for a GitHub repository
def get_default_branch(repo):
    try:
        url = f"{BASE_URL}{repo}"
        response = requests.get(url)
        response.raise_for_status()
        repo_data = response.json()
        default_branch = repo_data["default_branch"]
        return default_branch
    except Exception as e:
        print(f"Error fetching default branch for {repo}: {str(e)}")
        return None

# Function to get the timestamp of the last commit date for a GitHub repository
def get_last_commit_timestamp(repo):
    default_branch = get_default_branch(repo)
    if default_branch:
        try:
            url = f"{BASE_URL}{repo}/commits/{default_branch}"
            response = requests.get(url)
            response.raise_for_status()
            commit_data = response.json()
            last_commit_date = commit_data["commit"]["committer"]["date"]
            # Convert last_commit_date to Unix timestamp
            timestamp = datetime.strptime(last_commit_date, '%Y-%m-%dT%H:%M:%SZ').timestamp()
            return int(timestamp)
        except Exception as e:
            print(f"Error fetching last commit date for {repo}: {str(e)}")
    return None

# Path to the projects.json file
projects_json_path = os.path.expanduser("~/GitHub/jonasjones.dev/src/routes/projects/projects.json")

# Load the existing projects.json file
with open(projects_json_path, "r") as file:
    projects_data = json.load(file)

# Update the last_update (Unix timestamp) for each project
for project in projects_data:
    gh_api = project.get("gh_api")
    if gh_api:
        last_commit_timestamp = get_last_commit_timestamp(gh_api)
        if last_commit_timestamp:
            project["last_update"] = last_commit_timestamp

# Save the updated data back to the projects.json file
with open(projects_json_path, "w") as file:
    json.dump(projects_data, file, indent=2)

print("Updated projects.json with last_update (Unix timestamp) information.")
