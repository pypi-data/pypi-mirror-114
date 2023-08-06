import random
import string
from pathlib import Path
import typer
from configparser import ConfigParser
import pygit2
import asyncio
from aiohttp.client_exceptions import ClientConnectorError
from typing import Coroutine

from tym.models import AuthenticationError, RepoError, RequestError, VersionError
from tym import constants


def typer_error(error_message: str):
    typer.echo(
        typer.style("Error:", fg=typer.colors.RED, bold=True) + " " + error_message,
        err=True,
    )


def typer_success(success_message: str):
    typer.echo(typer.style("✔", fg=typer.colors.GREEN) + "  " + success_message)


def typer_instructions(instruction: str) -> str:
    return typer.style(instruction, fg=typer.colors.YELLOW)


def get_random_string(length) -> str:
    # Generate random strings with lowercase letters
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def get_app_config_filepath() -> Path:
    app_dir = typer.get_app_dir(constants.APP_NAME)
    return Path(app_dir) / constants.CONFIG_FILENAME


def get_auth_config() -> ConfigParser:
    app_config_filepath = get_app_config_filepath()
    # Check if config is created - required for storing auth info
    if not app_config_filepath.is_file():
        raise AuthenticationError({"detail": "Auth config file does not exist."})
    config = ConfigParser()
    config.read(app_config_filepath)
    return config


def get_repo_config_filepath() -> Path:
    git_dir = Path(pygit2.discover_repository("."))
    return git_dir / constants.CONFIG_FILENAME


def get_repo_config() -> str:
    repo_config_filepath = get_repo_config_filepath()
    # Check if config is created - required for storing repo info
    if not repo_config_filepath.is_file():
        raise RepoError({"detail": "Repo config file does not exist."})
    config = ConfigParser()
    config.read(repo_config_filepath)
    return config


async def schedule_periodic_function(seconds: float, func: Coroutine, *args, **kwargs):
    while True:
        await asyncio.sleep(seconds)
        try:
            await func(*args, **kwargs)
        except asyncio.CancelledError:
            break
        except RequestError as e:
            typer.echo(
                f"Periodic function faced error <{str(e)}>. Tym will still continue to function."
            )
        except ClientConnectorError as e:
            typer.echo(
                f"Periodic function error <{str(e)}>. Check if your network connection is down. Tym will still continue to function."
            )


def assert_versions_compatible(client_version: str, backend_version: str):
    client_major, client_minor, client_patch = client_version.split(".")
    backend_major, backend_minor, backend_patch = backend_version.split(".")

    if client_major != backend_major:
        raise VersionError("Tym has released a new major version.")

    if client_minor != backend_minor:
        raise VersionError("Tym has released a new minor version.")

    if client_patch != backend_patch:
        typer.echo("Tym has released a new patch.")
        typer.echo(
            "Get the latest updates by running "
            + typer_instructions("pip install --upgrade tym")
            + "."
        )
