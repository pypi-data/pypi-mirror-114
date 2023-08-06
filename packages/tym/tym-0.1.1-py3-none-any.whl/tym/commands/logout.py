import typer
from configparser import ConfigParser

from tym.config_parser.authentication import (
    get_email,
    get_refresh_token,
    clear_auth_config,
)
from tym.commons import typer_success, get_app_config_filepath


def logout():
    app_config_filepath = get_app_config_filepath()
    # Check if config is created
    if not app_config_filepath.is_file():
        # User does not have a config file, which means they never logged in
        typer.echo("You are already logged out.")
        raise typer.Exit()

    # Read the config file to check if user is authenticated
    config = ConfigParser()
    config.read(app_config_filepath)
    try:
        get_refresh_token(config)
        email = get_email(config)
    except:
        typer.echo("You are already logged out.")
        raise typer.Exit()

    clear_auth_config(config)
    with app_config_filepath.open("w") as config_file:
        config.write(config_file)

    typer_success(
        "Logged out from " + typer.style(email, fg=typer.colors.CYAN, bold=True) + "."
    )
