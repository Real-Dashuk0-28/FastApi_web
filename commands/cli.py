import typer
from rich import print as rprint

# Создаем главное приложение
app = typer.Typer(
    name="bookmanager",
    help="Управление библиотекой книг",
    add_completion=False,
    rich_markup_mode="rich"
)

# Импортируем и добавляем команды приветствия
from commands.hello import hello_app

app.add_typer(hello_app, name="hello")


@app.callback()
def callback():
    rprint("📚 [green]Welcome to Book Manager![/green]")