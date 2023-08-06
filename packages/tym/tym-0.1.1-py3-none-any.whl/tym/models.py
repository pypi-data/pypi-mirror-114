from datetime import datetime
from typing import Optional, List, Tuple, Sequence, Any, Callable, Generator


class RequestError(Exception):
    def __init__(self, data: Optional[dict] = None):
        self.data = data

    def __str__(self) -> str:
        error_message = type(self).__name__
        if self.data != None:
            error_message += f" - {self.data}"
        return error_message


class AuthenticationError(RequestError):
    pass


class RepoError(RequestError):
    pass


class ServerError(Exception):
    pass


class VersionError(Exception):
    pass


class RepoState:
    Merged = "merged"
    Active = "active"
    Archived = "archived"
    Deleted = "deleted"
    Error = "error"


class TymRepo:
    def __init__(self, id: str, state: str, tym_remotes: List[str]):
        self.id = id
        self.state = state
        self.tym_remotes = tym_remotes
