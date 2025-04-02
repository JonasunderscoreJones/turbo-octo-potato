import os
import sys
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

VERBOSEPRINT = "-v" in sys.argv or "--verbose" in sys.argv
DONTDOWNLOAD = "-dd" in sys.argv or "--dont-download" in sys.argv
DONTUPDATEGH = "-du" in sys.argv or "--dont-update-github" in sys.argv

def verboseprint(string="", end="\n"):
    if VERBOSEPRINT:
        print(string, end=end)

verboseprint(f"Printing verbose logs")

# Load environment variables from .env file
load_dotenv()

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

# GitHub API base URL
BASE_URL = "https://api.github.com/repos/"

# Function to get the default branch name for a GitHub repository
def get_default_branch(repo, access_token):
    try:
        url = f"{BASE_URL}{repo}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        repo_data = response.json()
        default_branch = repo_data["default_branch"]
        verboseprint(f"[{repo}] Fetched default branch", end="\r")
        return default_branch
    except Exception as e:
        verboseprint(f"[{repo}] Error fetching default branch      ", end="\r")
        return None

# Function to get the timestamp of the last commit date for a GitHub repository
def get_last_commit_timestamp(repo, access_token):
    default_branch = get_default_branch(repo, access_token)
    if default_branch:
        url = f"{BASE_URL}{repo}/commits/{default_branch}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        commit_data = response.json()
        last_commit_date = commit_data["commit"]["author"]["date"]
        # Convert last_commit_date to Unix timestamp
        timestamp = datetime.strptime(last_commit_date, '%Y-%m-%dT%H:%M:%SZ').timestamp()
        verboseprint(f"[{repo}] Fetched last-commit-timestamp", end="\r")
        return int(timestamp)
    return None

def get_last_release_version(repo, access_token):
    try:
        url = f"{BASE_URL}{repo}/releases/latest"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)

        # Check if the response status code indicates that the release does not exist
        if response.status_code == 404:
            return None

        response.raise_for_status()
        release_data = response.json()
        last_release_version = release_data["tag_name"]
        verboseprint(f"[{repo}] Fetched last project release version", end="\r")
        return last_release_version
    except Exception as e:
        print(f"[{repo}] Error fetching last release version", end="\r")
        return None

def get_languagages(repo, access_token):
    try:
        url = f"{BASE_URL}{repo}/languages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        languages_data = response.json()
        verboseprint(f"[{repo}] Fetched repo language statistics    ", end="\r")
        verboseprint(f"[{repo}] Done!                               ")
        return languages_data
    except Exception as e:
        print(f"[{repo}] Error fetching languages           ", end="\n")
        return None

def main():
    # Path to the projects.json file
    projects_json_path = os.path.expanduser("~/.cache/gh-projects/projects.json")
    # create the directory if it doesn't exist
    os.makedirs(os.path.dirname(projects_json_path), exist_ok=True)

    if not DONTDOWNLOAD:
        # fetch the projects.json file from https://cdn.jonasjones.dev/api/projects/projects.json
        projects_json_url = "https://cdn.jonasjones.dev/api/projects/projects.json"
        projects_json = requests.get(projects_json_url)
        with open(projects_json_path, "wb") as file:
            file.write(projects_json.content)

        verboseprint(f"Fetched projects.json file")
    elif not os.path.exists("~/.cache/gh-projects/projects.json"):
        FileNotFoundError("File 'projects.json' not found. Cannot proceed without \
                        downloading it. Remove '-dd' or '--dontdownload' from the launch arguments.")
    else:
        print("Skipping download of 'projects.json'")

    # Load the existing projects.json file
    with open(projects_json_path, "r") as file:
        projects_data = json.load(file)

    if not DONTUPDATEGH:
        print("Fetching Repo data...")

        # Update the last_update (Unix timestamp) for each project
        for project in projects_data:
            gh_api = project.get("gh_api")
            if gh_api:
                last_commit_timestamp = get_last_commit_timestamp(gh_api, GITHUB_API_TOKEN)
                last_release_version = get_last_release_version(gh_api, GITHUB_API_TOKEN)
                if last_commit_timestamp:
                    project["last_update"] = last_commit_timestamp
                else:
                    project["last_update"] = 0
                if last_release_version:
                    project["version"] = last_release_version.replace("v", "")
                languages = get_languagages(gh_api, GITHUB_API_TOKEN)
                if languages:
                    project["languages"] = languages
    else:
        print("Skipping Github updates...")

    # remove first element
    projects_data.pop(0)

    # sort projects alphabetically
    projects_data = sorted(projects_data, key=lambda x: x['last_update'], reverse=True)

    # add a first element to the list that holds the date of the last update
    projects_data.insert(0, {"last_update": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + " UTC"})

    # Save the updated data back to the projects.json file
    with open(projects_json_path, "w") as file:
        json.dump(projects_data, file, indent=2)

    print("Updated projects.json\nUploading to cdn...")

    os.system(f"rclone copy {projects_json_path} cdn:cdn/api/projects/")

    print("Uploaded projects.json to cdn")


if __name__ == "__main__":
    main()