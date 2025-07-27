import os
from git import Repo
from urllib.parse import urlparse

def clone_repo(repo_url: str) -> str:
    repo_name = os.path.splitext(os.path.basename(urlparse(repo_url).path))[0]
    cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
    repo_path = os.path.join(cache_dir, repo_name)
    if os.path.exists(repo_path):
        return repo_path  # Already cloned
    Repo.clone_from(repo_url, repo_path)
    return repo_path 