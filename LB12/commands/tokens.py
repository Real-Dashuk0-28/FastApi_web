import typer
from typing import Annotated, Optional
from rich import print as rprint
from rich.table import Table
from rich.prompt import Prompt

# Импортируем хелпер для токенов (относительный импорт)
from auth.services.redis_tokens_helper import RedisTokensHelper

tokens_app = typer.Typer(
    name="tokens",
    help="Управление API токенами",
    rich_markup_mode="rich",
)

tokens_helper = RedisTokensHelper()


@tokens_app.command()
def check(
        token: Annotated[str, typer.Argument(help="API токен для проверки")]
):
    """Проверяет существование API токена"""
    if tokens_helper.token_exists(token):
        rprint(f"✅ [green]Токен существует:[/green] [bold]{token}[/bold]")
    else:
        rprint(f"❌ [red]Токен не найден:[/red] [bold]{token}[/bold]")


@tokens_app.command(name="list")
def list_tokens():
    """Показывает список всех API токенов"""
    tokens = tokens_helper.get_tokens()

    if not tokens:
        rprint("📭 [yellow]Нет активных токенов[/yellow]")
        return

    table = Table(title="📋 Список API токенов", style="cyan")
    table.add_column("№", style="bold", width=4)
    table.add_column("Токен", style="green")
    table.add_column("Длина", style="yellow", justify="right")

    for i, token in enumerate(tokens, 1):
        table.add_row(str(i), token, str(len(token)))

    rprint(table)
    rprint(f"\n[bold]Всего токенов:[/bold] [green]{len(tokens)}[/green]")


@tokens_app.command()
def create():
    """Создает новый API токен и сохраняет его"""
    new_token = tokens_helper.generate_and_save_token()
    rprint(f"✨ [green]Создан новый токен:[/green]")
    rprint(f"[bold cyan]{new_token}[/bold cyan]")
    rprint("\n[dim]Сохраните этот токен — он больше не будет показан[/dim]")


@tokens_app.command()
def add(
        token: Annotated[str, typer.Argument(help="Токен для добавления")]
):
    """Добавляет переданный токен в базу данных"""
    if tokens_helper.token_exists(token):
        rprint(f"⚠️ [yellow]Токен уже существует:[/yellow] [bold]{token}[/bold]")
        raise typer.Exit(code=1)

    tokens_helper.add_token(token)
    rprint(f"✅ [green]Токен добавлен:[/green] [bold]{token}[/bold]")


@tokens_app.command()
def rm(
        token: Annotated[str, typer.Argument(help="Токен для удаления")],
        force: Annotated[
            Optional[bool],
            typer.Option("--force", "-f", help="Принудительное удаление без подтверждения")
        ] = False,
):
    """Удаляет токен из базы данных"""
    if not tokens_helper.token_exists(token):
        rprint(f"❌ [red]Токен не найден:[/red] [bold]{token}[/bold]")
        raise typer.Exit(code=1)

    if not force:
        confirm = Prompt.ask(
            f"⚠️  Удалить токен [bold]{token}[/bold]? [y/N]",
            default="n"
        )
        if confirm.lower() not in ["y", "yes"]:
            rprint("[yellow]Операция отменена[/yellow]")
            return

    tokens_helper.delete_token(token)
    rprint(f"🗑️  [red]Токен удален:[/red] [bold]{token}[/bold]")