# github_api.py
import requests

def get_all_repos(owner, headers, is_org=False):
    all_repos = []
    page = 1
    while True:
        url = f"https://api.github.com/{'orgs' if is_org else 'users'}/{owner}/repos"
        resp = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        if resp.status_code != 200:
            print(f"[get_all_repos] Error {resp.status_code}: {resp.text}")
            break

        data = resp.json()
        if not data:
            break  # no more repos
        for repo_obj in data:
            all_repos.append(repo_obj["name"])
        page += 1

    return all_repos

def get_repo_data(owner, repo, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"[get_repo_data] Error {resp.status_code}: {resp.text}")
        return None

import base64
import requests

def get_file_content(owner, repo, path, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        j = resp.json()
        if j.get("encoding") == "base64":
            # Decode to bytes
            decoded_bytes = base64.b64decode(j["content"])
            # Then decode to a *string*
            return decoded_bytes.decode("utf-8", errors="ignore")
    return None

