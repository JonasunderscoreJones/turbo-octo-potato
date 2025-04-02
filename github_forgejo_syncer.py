import requests
import os
import dotenv

# Load the environment variables
dotenv.load_dotenv()

# Configuration: Set your GitHub and Forgejo credentials and URLs
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
FORGEJO_USERNAME = os.getenv('FORGEJO_USERNAME')
FORGEJO_API_URL = os.getenv('FORGEJO_API_URL')
FORGEJO_TOKEN = os.getenv('FORGEJO_TOKEN')

REPO_BLACKLIST = ["ZtereoMUSIC", "nicer-skies", "epr_grader"]

# Fetch repositories from GitHub
def get_github_repositories():
    github_url = f'https://api.github.com/users/{GITHUB_USERNAME}/repos'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    repos = []
    page = 1

    while True:
        response = requests.get(github_url, headers=headers, params={'page': page, 'per_page': 100})
        if response.status_code != 200:
            print(f"Error fetching GitHub repositories: {response.text}")
            break

        data = response.json()
        if not data:  # No more repositories
            break

        repos.extend(data)
        page += 1

    return repos

# Check if a repository exists on Forgejo
def check_forgejo_repo_exists(repo_name):
    forgejo_url = f'{FORGEJO_API_URL}/repos/{FORGEJO_USERNAME}/{repo_name}'
    headers = {'Authorization': f'token {FORGEJO_TOKEN}'}
    response = requests.get(forgejo_url, headers=headers)

    if response.status_code == 200:
        return True  # Repo exists
    elif response.status_code == 404:
        return False  # Repo does not exist
    else:
        print(f"Error checking repository on Forgejo: {response.text}")
        return False

# Create a mirror repository on Forgejo
def create_forgejo_repo_mirror(github_repo):
    forgejo_url = f'{FORGEJO_API_URL}/repos/migrate'
    headers = {'Authorization': f'token {FORGEJO_TOKEN}', 'Content-Type': 'application/json'}
    
    # Prepare the payload
    payload = {
        'clone_addr': github_repo['clone_url'],
        'repo_name': github_repo['name'],
        'private': github_repo['private'],
        'mirror': True,
        'description': github_repo.get('description', ''),
    }
    
    response = requests.post(forgejo_url, json=payload, headers=headers)
    
    if response.status_code == 201:
        print(f"Created mirror for {github_repo['name']}")
    else:
        print(f"Error creating mirror for {github_repo['name']}: {response.text}")

# Main script
def main():
    print("Fetching GitHub repositories...")
    github_repos = get_github_repositories()
    
    for github_repo in github_repos:
        repo_name = github_repo['name']
        print(f"Checking if {repo_name} exists on Forgejo...")

        if repo_name in REPO_BLACKLIST:
            print(f"Repository {repo_name} is blacklisted. Skipping.")
        elif not check_forgejo_repo_exists(repo_name):
            print(f"Repository {repo_name} does not exist on Forgejo. Creating mirror...")
            create_forgejo_repo_mirror(github_repo)
        else:
            print(f"Repository {repo_name} already exists on Forgejo. Skipping.")

if __name__ == '__main__':
    main()
