import typer
from configparser import ConfigParser

from tym.adapter import Adapter
from tym.config_parser.authentication import set_auth_config, get_email
from tym.models import RequestError
from tym.commons import typer_error, typer_success, get_app_config_filepath


async def login(adapter: Adapter):
    app_config_filepath = get_app_config_filepath()
    # Check if user is logged in
    config = None
    if app_config_filepath.is_file():
        # Authenticate with server
        config = ConfigParser()
        config.read(app_config_filepath)
        try:
            adapter.initialize_auth(config)
            await adapter.get_access_token()
            email = get_email(config)
            typer.echo(
                "You are already logged in as "
                + typer.style(email, fg=typer.colors.CYAN, bold=True)
                + "."
            )
            raise typer.Exit(0)
        except typer.Exit:
            raise typer.Exit(0)
        except Exception:
            pass

    # User needs to be authenticated
    secret_token = typer.prompt("Secret token", hide_input=True)

    # TODO: Authenticate with the backend properly
    try:
        refresh_token, email = await adapter.get_refresh_token_and_email_hacky(
            secret_token
        )
    except RequestError:
        typer.echo("Oops... hacky authentication with the backend failed", err=True)
        typer_error("Failed to login. Please try again.")
        raise typer.Exit(1)
    except Exception as e:
        typer_error(str(e))
        raise typer.Exit(1)

    if config == None:
        config = ConfigParser()

    set_auth_config(config, email, refresh_token)

    if not app_config_filepath.parent.exists():
        app_config_filepath.parent.mkdir(parents=True, exist_ok=True)

    with app_config_filepath.open("w") as config_file:
        config.write(config_file)

    typer.echo(
        "\nWelcome to Tym! 🎉",
    )
    typer_success("Logged in as " + typer.style(email, fg=typer.colors.CYAN, bold=True))
