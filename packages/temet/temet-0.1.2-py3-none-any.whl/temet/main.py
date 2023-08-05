import typer
from .utils.gen_structure import gen_fastapi

app = typer.Typer()


@app.callback()
def callback():
    """
    justTemet
    """


@app.command()
def fastapi():
    """
    Create a FastAPI structure
    """
    gen_fastapi()
    typer.echo("File structure created")
