"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Django AIML."""


if __name__ == "__main__":
    main(prog_name="django-aiml")  # pragma: no cover
