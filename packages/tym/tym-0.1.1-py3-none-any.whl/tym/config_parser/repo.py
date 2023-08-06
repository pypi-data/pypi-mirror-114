from json.decoder import JSONDecodeError
from typing import List
from configparser import ConfigParser
import json

from tym.models import RepoError


def get_tym_repo_id(repo_config: ConfigParser) -> str:
    if "repo" not in repo_config:
        raise RepoError({"detail": "Repo has not been initialized."})
    repo_section = repo_config["repo"]
    if "id" not in repo_section:
        raise RepoError({"detail": "Repo id is missing."})
    return repo_section["id"]


def get_tym_repo_client_id(repo_config: ConfigParser) -> str:
    if "repo" not in repo_config:
        raise RepoError({"detail": "Repo has not been initialized."})
    repo_section = repo_config["repo"]
    if "client_id" not in repo_section:
        raise RepoError({"detail": "Client id is missing."})
    return repo_section["client_id"]


def get_tym_repo_remotes(repo_config: ConfigParser) -> str:
    if "repo" not in repo_config:
        raise RepoError({"detail": "Repo has not been initialized."})
    repo_section = repo_config["repo"]
    if "remotes" not in repo_section:
        raise RepoError({"detail": "Remotes are not set for the repo."})
    try:
        remotes = json.loads(repo_section["remotes"])
    except JSONDecodeError:
        raise RepoError({"detail": "Could not decode remotes."})
    return remotes


def clear_repo_config(config: ConfigParser):
    # Used for resetting the repo
    if "repo" in config:
        repo_section = config["repo"]
        if "id" in repo_section:
            del repo_section["id"]
        if "remotes" in repo_section:
            del repo_section["remotes"]
    else:
        config["repo"] = {}


def set_tym_repo_config_id(config: ConfigParser, repo_id: str):
    if "repo" in config:
        config["repo"]["id"] = repo_id
    else:
        config["repo"] = {"id": repo_id}


def set_tym_repo_config_remotes(config: ConfigParser, tym_remotes: List[str]):
    tym_remotes_str = json.dumps(tym_remotes)
    if "repo" in config:
        config["repo"]["remotes"] = tym_remotes_str
    else:
        config["repo"] = {"remotes": tym_remotes_str}


def set_tym_repo_client_id(config: ConfigParser, client_id: str):
    if "repo" in config:
        config["repo"]["client_id"] = client_id
    else:
        config["repo"] = {"client_id": client_id}
