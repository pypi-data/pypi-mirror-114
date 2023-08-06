from typing import List, Tuple
from pathlib import Path
from simple_term_menu import TerminalMenu
from configparser import ConfigParser
import typer
import pygit2

from tym.commons import typer_error, typer_success, get_repo_config_filepath
from tym.config_parser.repo import (
    set_tym_repo_config_id,
    set_tym_repo_config_remotes,
)
from tym.models import RepoError, RequestError
from tym.adapter import Adapter


def select_tym_remotes(repo: pygit2.Repository) -> Tuple[List[str], List[str]]:
    typer.echo(
        "Select a git remote server that you will use to sync your Tym data. (i.e. origin)"
    )
    remote_names = [remote.name for remote in repo.remotes]
    terminal_menu = TerminalMenu(
        remote_names,
        multi_select=True,
        show_multi_select_hint=True,
    )
    confirmed_selection = False
    chosen_remotes = None
    failed_attempts = 0
    while not confirmed_selection:
        if failed_attempts >= 3:
            raise typer.Exit(1)
        terminal_menu.show()
        chosen_remotes = terminal_menu.chosen_menu_entries
        if chosen_remotes == None:
            typer_error("You must select at least one remote to continue.")
            failed_attempts += 1
        else:
            selected_remotes_str = ",".join(chosen_remotes)
            confirmed_selection = typer.confirm(
                f"You have selected [{selected_remotes_str}] as your tym remote. Confirm?"
            )
    tym_remote_names = list(chosen_remotes)
    tym_remote_urls = [
        repo.remotes[remote_name].url for remote_name in tym_remote_names
    ]
    return tym_remote_names, tym_remote_urls


async def init(adapter: Adapter, token: str):
    repo_config_filepath = get_repo_config_filepath()
    is_initialized = False
    config = ConfigParser()
    # First check if repo has already been initialized.
    if repo_config_filepath.is_file():
        config.read(repo_config_filepath)
        try:
            new_config = await adapter.initialize_repo(config)
            if new_config:
                config = new_config
                with repo_config_filepath.open("w") as config_file:
                    config.write(config_file)
            is_initialized = True
        except RepoError as e:
            if "code" in e.data:
                raise e

    repo_path = Path(pygit2.discover_repository("."))
    repo = pygit2.Repository(repo_path)
    if len(repo.remotes) == 0:
        typer_error(
            "Your repo needs to have at least one remote git server to use tym."
        )
        raise typer.Exit(1)

    # Check if a new repo should be created
    if len(token) == 0:
        if is_initialized:
            typer_error("Repo has already been initialized by Tym.")
            raise typer.Exit(1)
        # Check if user wants to create a new repo
        is_existing_repo = typer.confirm("Are you connecting to an existing tym repo?")
        if not is_existing_repo:
            # Create a new repo
            repo_name = typer.prompt("Enter new repo name")
            all_remote_urls = [remote.url for remote in repo.remotes]
            tym_remotes, tym_remote_urls = select_tym_remotes(repo)
            try:
                repo_id = await adapter.create_repo(
                    repo_name, all_remote_urls, tym_remote_urls
                )
                set_tym_repo_config_id(config, repo_id)
                set_tym_repo_config_remotes(config, tym_remotes)
                with repo_config_filepath.open("w") as config_file:
                    config.write(config_file)
                typer_success(f"Repo {repo_name} created and initialized.")
                raise typer.Exit()
            except RequestError as e:
                detail = f" <{str(e)}>"
                error_msg = f"Could not create repo.{detail} Please try again."
                typer_error(error_msg)
                raise typer.Exit(1)
        else:
            token = typer.prompt("Enter token from existing repo")

    # Connect this repo with the tym repo if not yet initialized
    # Otherwise, merge the current tym repo with the token's repo
    if is_initialized:
        # Merge
        confirm_merge = typer.confirm(
            "This repo already exist on tym.\nDo you want to merge it with another repo associated with this token?"
        )
        if not confirm_merge:
            raise typer.Exit()
        try:
            repo_id, repo_name = await adapter.merge_repo(token)
            set_tym_repo_config_id(config, repo_id)
            with repo_config_filepath.open("w") as config_file:
                config.write(config_file)
            typer_success(f"Merge successful. Initializing repo {repo_name}.")
            raise typer.Exit()
        except RequestError as e:
            detail = f" <{str(e)}>"
            error_msg = f"Could not merge repo.{detail} Please try again."
            typer_error(error_msg)
            raise typer.Exit(1)
    else:
        # Connect
        all_remote_urls = [remote.url for remote in repo.remotes]
        tym_remotes, tym_remote_urls = select_tym_remotes(repo)
        try:
            repo_id, repo_name = await adapter.connect_repo(
                token, all_remote_urls, tym_remote_urls
            )
            set_tym_repo_config_id(config, repo_id)
            set_tym_repo_config_remotes(config, tym_remotes)
            with repo_config_filepath.open("w") as config_file:
                config.write(config_file)
            typer_success(f"Repo {repo_name} connected and initialized.")
            raise typer.Exit()
        except RequestError as e:
            detail = f" <{str(e)}>"
            error_msg = f"Could not connect repo.{detail} Please try again."
            typer_error(error_msg)
            raise typer.Exit(1)
