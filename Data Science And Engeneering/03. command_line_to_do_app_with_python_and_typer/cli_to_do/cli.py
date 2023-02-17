"""This module provide the cli_to_cli CLI"""
# cli_to_do/cli.py

import typer

from pathlib import Path
from typing import List, Optional

from cli_to_do import ERRORS, __app_name__, __version__, config, database, cli_to_do


app = typer.Typer() #Create a Typer apllication

# Initialize the database
@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH), # If user doesn't imput a custom location, default will be used
        "--db-path", "-db", # Extended and shorted option to call the function from command line
        prompt=f"Imput the to-do database location. If none is given  {str(database.DEFAULT_DB_FILE_PATH)} will be used as defualt"
    ),
) -> None:
    """ Intialize the database """
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creation of config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The to-do databse is {db_path}", fg=typer.colors.GREEN)

def get_todoer() -> cli_to_do.Todoer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please, run "cli_to_to init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return cli_to_do.Todoer(db_path)
    else:
        typer.secho(
            'Database not found. Please run "cli_to_do init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command(name="list")
def list_all() -> None:
    """List all to-dos."""
    todoer = get_todoer()
    todo_list = todoer.get_todo_list()
    if len(todo_list) == 0:
        typer.secho(
            "There are no tasks in the to-do list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nto-do list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Priority  ",
        "| Done  ",
        "| Description  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, todo in enumerate(todo_list, 1):
        desc, priority, done = todo.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)

@app.command()
def add(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    todoer = get_todoer()
    todo, error = todoer.add(description, priority)
    if error:
        typer.secho(
            f'Adding to-do failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""to-do: "{todo['Description']}" has been added"""
            f"""with priority {priority}""",
            fg=typer.colors.GREEN,
        )

@app.command()
def remove(
    todo_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--force", "-f",
        help="Force deletion without confirmation"
    ),
) -> None:
    todoer = get_todoer()

    def _remove():
        todo, error = todoer.remove(todo_id)
        if error:
            typer.secho(
                f"Removing to-do # {todo_id} failed with {ERRORS[error]}",
                fg = typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"# {todo_id} removed",
                fg = typer.colors.GREEN,
            )
    if force:
        _remove()
    else:
        todo_list = todoer.get_todo_list()
        try:
            todo = todo_list[todo_id - 1]
        except IndexError:
            typer.secho("Invalid todo id", fg=typer.colors.RED)
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Delete # {todo_id}: {todo['Description']}?"
        )
        if delete:
            _remove()
        else:
            typer.secho("Operation canelled", fg=typer.colors.GREEN)


@app.command(name="complete")
def set_done(todo_id: int = typer.Argument(...)) -> None:
    todoer = get_todoer()
    todo, error = todoer.set_done(todo_id)
    if error:
        typer.secho(
            f"Couldn't complete to-do #{todo_id} because {ERRORS[error]}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"To do # {todo_id} '{todo['Description']}' completed",
            fg=typer.colors.GREEN
        )

def _version_callback(value: bool) -> None:
    """
        If value is True, print the application's version
    """
    if value:
        typer.echo(f"{__app_name__} v.{__version__}") ####### Sostituire con print from rich module
        raise typer.Exit() # Used to exit the application cleanly
 
# Allow user to retrive the apllication's version
@app.callback() 
def main( 
    version: Optional[bool] = typer.Option( # provare a sostituire con  X | None (or Union[X, None]).
        None, # None is passed as default value
        "--version", "-v", # command-line name for the version option
        help="Show the apllication's version and exit.", # Provides a help message for the vesion option
        callback = _version_callback, # calls the _version_collaback function
        is_eager = True # Tells typer that versione command-line option has preceence over other command
    )
) -> None:
    return