""" cli_to_do entry point script."""
# cli_to_do/__main__.py

from cli_to_do import cli, __app_name__


def main():
    """
    Passing __app_name__ ensure the user will recive the correct app name
    when running --help option on the command line
    """
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()