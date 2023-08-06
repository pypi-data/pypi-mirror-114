from typing import Optional
import click
import logging
import enlighten
import time
from .timetable import TimeTable


@click.command()
def demo():
    click.echo("""
Please give a schema file:

    $ python -m schemdule --schema schema.py
""")

    demo_schema = """
from datetime import datetime, timedelta
now = datetime.now()
at((now + timedelta(seconds=3)).time(), "Demo event")
cycle((now + timedelta(seconds=5)).time(), 
    (now + timedelta(seconds=20)).time(),
    "00:00:05",
    "00:00:05", "Demo cycle")

prompter.useConsole()
"""

    click.echo("A demo schema:\n")
    click.echo("\n".join(map(lambda x: "    " + x,
               demo_schema.strip().splitlines())))

    click.echo("\nScheduling...")

    tt = TimeTable()
    tt.load(demo_schema)

    tt.schedule()


@click.command()
@click.option("--preview/--no-preview", default=False, help="Preview the built timetable.")
@click.argument("schema", type=click.Path(exists=True))
def run(schema: str, preview: bool = False) -> None:
    logger = logging.getLogger("run")

    click.echo("Welcome to Schemdule!")

    tt = TimeTable()

    with open(schema, encoding="utf8") as f:
        tt.load(f.read())

    if preview:
        for item in sorted(tt.items):
            click.echo(f"{item.message} @ {item.time}")
    else:
        tt.schedule()


@click.group()
@click.option('-v', '--verbose', count=True, default=0, type=click.IntRange(0, 4))
def main(verbose: int = 0) -> None:
    """Schemdule (https://github.com/StardustDL/schemdule)

A tiny tool using script as schema to schedule one day and remind you to do something during a day.
"""

    logging.basicConfig(level={
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
        3: logging.DEBUG,
        4: logging.NOTSET
    }[verbose])


main.add_command(run)
main.add_command(demo)

if __name__ == '__main__':
    main()
