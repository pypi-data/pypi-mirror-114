from configparser import ConfigParser
import time
import re
from typing import Optional, Tuple, List
from pathlib import Path
import aiohttp
from aiohttp.client_exceptions import ClientOSError
import platform
import pygit2
import typer

from tym import constants
from tym.config_parser.repo import (
    get_tym_repo_client_id,
    get_tym_repo_id,
    get_tym_repo_remotes,
    set_tym_repo_client_id,
    set_tym_repo_config_id,
)
from tym.config_parser.authentication import get_email, get_refresh_token
from tym.models import AuthenticationError, RepoState, RequestError, RepoError, TymRepo


# Goal of adapter is to abstract away communication with the outside world
class Adapter:
    def __init__(self, http_session: aiohttp.ClientSession):
        self.http_session = http_session
        self.run_watcher = True
        self.max_request_retrys = 10

    def initialize_auth(self, auth_config: ConfigParser):
        self.refresh_token = get_refresh_token(auth_config)
        email = get_email(auth_config)
        email_username = email[: email.rindex("@")]
        self.username = re.sub("\W", "", email_username)
        self.token_expiration_time = 0
        self.access_token = ""

    async def initialize_repo(
        self, repo_config: ConfigParser
    ) -> Optional[ConfigParser]:
        config_changed = False
        repo_id = get_tym_repo_id(repo_config)
        tym_remotes = get_tym_repo_remotes(repo_config)
        repo_state = await self.get_repo_state(repo_id)
        # Repo is in merged state and needs to be resolved.
        if repo_state == RepoState.Merged:
            typer.echo("Your current repo has been merged.")
            typer.echo("Automatically resolving merged repo now.")
            new_repo_id = await self.resolve_merged_repo(repo_id)
            typer.echo("Merged repo successfully resolved.\n")
            if new_repo_id != repo_id:
                repo_id = new_repo_id
                set_tym_repo_config_id(repo_config, repo_id)
                config_changed = True
                repo_state = RepoState.Active
        if repo_state != RepoState.Active:
            raise RepoError(
                {
                    "detail": f"Current repo is in {repo_state} state.",
                    "code": "inactive-repo",
                }
            )
        self.repo = TymRepo(id=repo_id, state=repo_state, tym_remotes=tym_remotes)
        try:
            self.client_id = get_tym_repo_client_id(repo_config)
            await self.update_repo_client()
        except (RepoError, RequestError):
            self.client_id = await self.create_repo_client()
            set_tym_repo_client_id(repo_config, self.client_id)
            config_changed = True
        return repo_config if config_changed else None

    # Common methods
    async def request_backend(
        self, path: str, method: str, **kwargs
    ) -> Tuple[int, Optional[dict]]:
        method_map = {
            "POST": self.http_session.post,
            "GET": self.http_session.get,
            "PUT": self.http_session.put,
            "DELETE": self.http_session.delete,
        }
        if method.upper() not in method_map:
            raise RequestError({"detail": f"Requested {method} method is not valid."})
        method_func = method_map[method.upper()]
        url = constants.BACKEND_HOSTNAME + path
        for _ in range(self.max_request_retrys):
            try:
                async with method_func(url, **kwargs) as resp:
                    try:
                        data = await resp.json()
                        return resp.status, data
                    except:
                        text = await resp.text()
                        return resp.status, text
            except ClientOSError:
                pass
        raise RequestError({"detail": "Could not reach Tym server."})

    async def auth_headers(self) -> dict:
        access_token = await self.get_access_token()
        header = {"Authorization": f"Bearer {access_token}"}
        if hasattr(self, "repo"):
            header["Repo-Id"] = self.repo.id
        return header

    # Specific methods
    async def get_backend_version(self) -> str:
        status, data = await self.request_backend("/client/version", "GET")
        if status != 200:
            raise RequestError(data)
        return data["version"]

    async def get_access_token(self) -> str:
        # get new access token if expired
        current_time = time.time()
        if current_time > self.token_expiration_time:
            url = constants.RENEW_TOKEN_URL
            params = {"key": constants.FIREBASE_API_KEY}
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            }
            async with self.http_session.post(url, params=params, data=data) as resp:
                if resp.status != 200:
                    raise AuthenticationError(
                        {"detail": "Failed to acquire access token."}
                    )
                try:
                    data = await resp.json()
                    expires_in = int(data["expires_in"])
                    self.token_expiration_time = current_time + expires_in
                    self.access_token = data["access_token"]
                except:
                    raise AuthenticationError(
                        {"detail": "Unexpected access token response."}
                    )
        return self.access_token

    async def get_repo_state(self, repo_id: str) -> str:
        headers = await self.auth_headers()
        headers["Repo-Id"] = repo_id
        status, data = await self.request_backend("/repo/state", "GET", headers=headers)
        if status != 200:
            raise RequestError(data)
        return data["state"]

    async def create_repo(
        self, repo_name: str, all_remote_urls: List[str], tym_remote_urls: List[str]
    ) -> str:
        headers = await self.auth_headers()
        params = {
            "name": repo_name,
            "all_remote_urls": all_remote_urls,
            "tym_remote_urls": tym_remote_urls,
        }
        status, data = await self.request_backend(
            "/repo/create", "POST", params=params, headers=headers
        )
        if status != 201:
            raise RequestError(data)
        return data["repo_id"]

    async def merge_repo(self, token: str) -> Tuple[str, str]:
        headers = await self.auth_headers()
        params = {"token": token}
        status, data = await self.request_backend(
            "/repo/merge", "POST", params=params, headers=headers
        )
        if status != 200:
            raise RequestError(data)
        return data["main_repo_id"], data["name"]

    async def connect_repo(
        self, token: str, all_remote_urls: List[str], tym_remote_urls: List[str]
    ) -> Tuple[str, str]:
        headers = await self.auth_headers()
        params = {
            "token": token,
            "all_remote_urls": all_remote_urls,
            "tym_remote_urls": tym_remote_urls,
        }
        status, data = await self.request_backend(
            "/repo/connect", "PUT", params=params, headers=headers
        )
        if status != 200:
            raise RequestError(data)
        return data["repo_id"], data["name"]

    async def generate_repo_token(self) -> Tuple[str, str]:
        headers = await self.auth_headers()
        status, data = await self.request_backend(
            "/repo/token/create", "POST", headers=headers
        )
        if status != 201:
            raise RequestError(data)
        return data["token"], data["expires_in_days"]

    async def resolve_merged_repo(self, repo_id: str) -> str:
        headers = await self.auth_headers()
        max_iterations = 100
        current_repo_id = repo_id
        for _ in range(max_iterations):
            headers["Repo-Id"] = current_repo_id
            status, data = await self.request_backend(
                "/repo/resolve_merged_state", "POST", headers=headers
            )
            if status != 200:
                raise RepoError(data)
            if "resolved" in data and data["resolved"]:
                return data["main_repo_id"]
        raise RepoError(
            {
                "detail": "Did not fully resolve the merged repo.",
                "code": "incomplete-resolution",
            }
        )

    async def create_repo_client(self) -> str:
        headers = await self.auth_headers()
        repo_path = Path(pygit2.discover_repository("."))
        params = {
            "platform": platform.platform(),
            "node_name": platform.node(),
            "python_version": platform.python_version(),
            "repo_directory": str(repo_path.parent),
        }
        status, data = await self.request_backend(
            "/repo/client/create", "POST", params=params, headers=headers
        )
        if status != 200:
            raise RequestError(data)
        return data["id"]

    async def update_repo_client(self, port: Optional[int] = None):
        headers = await self.auth_headers()
        params = {"client_id": self.client_id}
        if port != None:
            params["port"] = port
        status, data = await self.request_backend(
            "/repo/client/update", "PUT", params=params, headers=headers
        )
        if status != 200:
            raise RequestError(data)

    async def create_branch(self, branch_name: str):
        headers = await self.auth_headers()
        params = {"branch_name": branch_name}
        status, data = await self.request_backend(
            "/branch/create", "POST", params=params, headers=headers
        )
        if status != 201:
            raise RequestError(data)

    async def update_branch(self, branch_name: str):
        headers = await self.auth_headers()
        params = {"branch_name": branch_name}
        status, data = await self.request_backend(
            "/branch/update", "PUT", params=params, headers=headers
        )
        if status != 200:
            raise RequestError(data)

    # HACK: Needs to be replaced
    async def get_refresh_token_and_email_hacky(
        self, secret_token: str
    ) -> Tuple[str, str]:
        params = {"client_token": secret_token}
        status, data = await self.request_backend("/oauth/token", "POST", params=params)
        if status != 200:
            raise RequestError(data)
        return data["refresh_token"], data["email"]

    def __str__(self) -> str:
        auth_initialized = hasattr(self, "refresh_token")
        repo_initialized = hasattr(self, "repo")
        return f"tym.Adapter - auth_initialized: {auth_initialized}, repo_initialized: {repo_initialized}"
