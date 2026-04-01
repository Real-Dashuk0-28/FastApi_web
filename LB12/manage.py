from commands import app
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from commands import app

def main():
    app()

if __name__ == "__main__":
    main()

#import typer
#from typing import Annotated
#from rich import print as rprint


#app = typer.Typer(
#    name="bookmanager",
#    help="Управление библиотекой книг",
#    add_completion=False,
#    # add_help_option=False, # для отключения опции --help
#    rich_markup_mode="rich",
#)


#@app.callback()
#def callback():
#    rprint("📚 [green]Welcome to Book Manager![/green]")


#@app.command(help="Приветствует пользователя по имени")
#def hello(name: Annotated[str, typer.Argument(help="Name to greet")]):
#    print(f"Hello {name}")


#def main():
#    app()


#if __name__ == "__main__":
#    main()