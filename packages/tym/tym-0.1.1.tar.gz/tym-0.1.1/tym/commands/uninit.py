from tym.models import RepoError
import typer

from tym.adapter import Adapter
from tym.config_parser.repo import (
    clear_repo_config,
    get_tym_repo_id,
    get_tym_repo_remotes,
)
from tym.commons import (
    typer_success,
    typer_error,
    get_repo_config,
    get_repo_config_filepath,
)


async def uninit(_: Adapter):
    try:
        repo_config = get_repo_config()
        get_tym_repo_id(repo_config)
        get_tym_repo_remotes(repo_config)
    except RepoError:
        typer_error("Repo is already uninitialized")
        raise typer.Exit()

    clear_repo_config(repo_config)
    repo_config_filepath = get_repo_config_filepath()
    with repo_config_filepath.open("w") as config_file:
        repo_config.write(config_file)
    typer_success("Repo uninitialized.")
