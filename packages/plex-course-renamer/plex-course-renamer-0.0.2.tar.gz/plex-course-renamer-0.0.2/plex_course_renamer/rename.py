import os
import click

@click.command()
def run():
    cwd = os.getcwd()

if __name__ == "__main__":
    run()