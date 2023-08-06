import typer

from tym.adapter import Adapter
from tym.commons import typer_success, typer_instructions


async def share(adapter: Adapter):
    # generate sharing token
    token, expires_in_days = await adapter.generate_repo_token()
    typer_success(
        f"Sharing token generated. Token will expire in {expires_in_days} day(s)."
    )
    typer.echo(
        "To connect, your collaborators need to run the following command in their repo directory:\n"
    )
    typer.echo(typer_instructions(f"tym init --token {token}"))
