import click

from app.builder.builder import Builder
from app.input_data.input_data_loader import InputData, InputDataLoader


@click.group()
def cli():
    """Validation commands."""


@click.command()
@click.argument("main_file")
@click.argument("output_dir")
def generate(main_file: str, output_dir: str):
    loader = InputDataLoader(main_file)
    data: InputData = loader.load()

    builder = Builder(data)
    builder.build_publication_files()

    a = True


cli.add_command(generate)


if __name__ == "__main__":
    cli()
