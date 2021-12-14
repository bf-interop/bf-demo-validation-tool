"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """PCC Data Exchange."""


if __name__ == "__main__":
    main(prog_name="pcc-data-exchange")  # pragma: no cover
