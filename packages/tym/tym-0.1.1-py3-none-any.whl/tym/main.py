from typing import Callable
import asyncio
import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
import pygit2
import typer

import tym
from tym.commons import (
    get_repo_config,
    get_repo_config_filepath,
    typer_error,
    get_auth_config,
    typer_instructions,
    assert_versions_compatible,
)
from tym.models import AuthenticationError, RepoError, RequestError, VersionError
from tym.adapter import Adapter
from tym.git_helpers import has_git, has_set_git_config_name, has_set_git_config_email
from tym import commands

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Tym is a realtime version control system compatible with git. Go to https://tym.so for more information.
    """
    if not has_git():
        typer_error("Git must be installed in the system to continue.")
        raise typer.Exit(code=1)

    repo_path = pygit2.discover_repository(".")
    if not ctx.invoked_subcommand in {"login", "logout"} and repo_path == None:
        typer_error("You have to be in a git repo to continue.")
        raise typer.Exit(code=1)

    if ctx.invoked_subcommand is None:
        start()


async def run_command(
    func: Callable, *args, use_auth: bool = True, use_repo: bool = True, **kwargs
):
    async with aiohttp.ClientSession() as session:
        try:
            adapter = Adapter(session)
            backend_version = await adapter.get_backend_version()
            assert_versions_compatible(tym.__version__, backend_version)
            if use_auth:
                print("Authenticating... ", end="", flush=True)
                auth_config = get_auth_config()
                adapter.initialize_auth(auth_config)
                await adapter.get_access_token()
                typer.secho("Done", fg=typer.colors.GREEN)
            if use_repo:
                print("Getting tym ready... ", end="", flush=True)
                repo_config = get_repo_config()
                new_repo_config = await adapter.initialize_repo(repo_config)
                if new_repo_config:
                    repo_config_filepath = get_repo_config_filepath()
                    with repo_config_filepath.open("w") as config_file:
                        new_repo_config.write(config_file)
                typer.secho("Done", fg=typer.colors.GREEN)
            await func(adapter, *args, **kwargs)
        except AuthenticationError as e:
            error_detail = e.data["detail"]
            typer_error(
                f"Failed to authenticate. {error_detail} Have you tried running "
                + typer_instructions("tym login")
                + "?"
            )
            raise typer.Exit(1)
        except RepoError as e:
            error_detail = e.data["detail"]
            if "code" in e.data:
                if e.data["code"] == "inactive-repo":
                    typer_error(
                        f"{error_detail} To tym repo config reset, run "
                        + typer_instructions("tym uninit")
                    )
                if e.data["code"] == "incomplete-resolution":
                    typer.echo(
                        f"{error_detail} Run your command again resolve the issue."
                    )
            else:
                typer_error(
                    f"Repo has not been initialized. {error_detail} Have you tried runnning "
                    + typer_instructions("tym init")
                    + "?"
                )
            raise typer.Exit(1)
        except RequestError as e:
            error_msg = str(e)
            typer_error(f"Oops... <{error_msg}>")
            raise typer.Exit(1)
        except ClientConnectorError as e:
            typer_error(str(e))
            raise typer.Exit(1)
        except VersionError as e:
            upgrade_instructions = (
                "To continue, please upgrade tym by running "
                + typer_instructions("pip install --upgrade tym")
            )
            typer_error(f"{str(e)}\n{upgrade_instructions}")
            raise typer.Exit(1)


@app.command()
def start():
    """
    Start real time git
    """
    if not has_set_git_config_name():
        typer_error(
            "Name is not set in Git config. To do so, run "
            + typer_instructions('git config --global user.name "FIRST_NAME LAST_NAME"')
        )
        raise typer.Exit(1)
    if not has_set_git_config_email():
        typer_error(
            "Email is not set in Git config. To do so, run "
            + typer_instructions("git config --global user.email MY_NAME@example.com")
        )
        raise typer.Exit(1)
    asyncio.run(run_command(commands.start))


@app.command()
def share():
    """
    Share the repo with others
    """
    asyncio.run(run_command(commands.share))


@app.command()
def init(token: str = typer.Option("")):
    """
    Initializing the repo with Tym
    """
    asyncio.run(run_command(commands.init, token, use_repo=False))


@app.command()
def uninit():
    """
    Uninitializing the repo with Tym
    """
    asyncio.run(run_command(commands.uninit, use_repo=False))


@app.command()
def login():
    """
    Login to Tym
    """
    asyncio.run(run_command(commands.login, use_auth=False, use_repo=False))


@app.command()
def logout():
    """
    Logout of Tym
    """
    commands.logout()


if __name__ == "__main__":
    app()
