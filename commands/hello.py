import typer
from typing import Annotated
from rich import print as rprint

# Создаем отдельный Typer для приветствий
hello_app = typer.Typer(
    name="hello",
    help="Команды для приветствия",
    rich_markup_mode="rich"
)

@hello_app.command()
def greet(name: Annotated[str, typer.Argument(help="Name to greet")]):
    """Приветствует пользователя по имени"""
    rprint(f"[red]Greet[/red] [bold]{name}[/bold]")

@hello_app.command()
def farewell(name: Annotated[str, typer.Argument(help="Name to say goodbye")]):
    """Прощается с пользователем"""
    rprint(f"Goodbye, [bold]{name}[/bold]! 👋")