import typer
from plumbum import local, FG

app = typer.Typer()


@app.command()
def run():
    local['coverage']['run', '-m', 'pytest', '-o', 'console_output_style=progress', '--forked', "--numprocesses=auto"] & FG
    local['coverage']['report', '-m'] & FG
