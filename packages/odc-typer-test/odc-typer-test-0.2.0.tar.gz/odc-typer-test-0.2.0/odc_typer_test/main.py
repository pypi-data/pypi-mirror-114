import typer
import random

app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome CLI user manager.
    """


@app.command()
def create(
    username: str = typer.Argument(
        ...,
        help="The name of user to create."
    )
):
    """
    Create a new user with USERNAME.
    """
    typer.echo(f"Creating user: {username}")


@app.command()
def delete(
    username: str = typer.Argument(
        ...,
        help="The name of user to delete."
    ),
    force: bool = typer.Option(
        ...,
        help="Force deletion without confirmation.",
        prompt="Are you sure?"
    )
):
    """
    Delete an existing user with USERNAME.

    If --force is not used, confirmation is required.
    """
    if force:
        typer.echo(f"Deleted user: {username}")
    else:
        typer.echo("Cancelled!")


@app.command()
def delete_all(
    force: bool = typer.Option(
        ...,
        help="Force deletion without confirmation.",
        prompt="Are you sure?"
    )
):
    """
    Delete all users in the database.

    If --force is not used, confirmation is required.
    """
    if force:
        typer.echo(f"Deleted all users.")
    else:
        typer.echo("Cancelled!")


def get_name():
    return random.choice(['Deadpool', 'Rick', 'Morty', 'Hiro'])


@app.command()
def init():
    """
    Initialize the user database.
    """
    typer.echo(f"Initializing user database as {get_name()}.")
