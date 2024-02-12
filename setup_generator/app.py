"""Command-line interface for managing Python setup."""

import click
from colorama import Fore, Style
from generator_file import SetupGenerator, load_config

@click.command()
@click.option('--init', is_flag=True, help='Initialize the setup with default values.')
@click.option('--build', is_flag=True, help='Build the package using setuptools.')
@click.option('--yes', is_flag=True, help='Automatically set defaults without prompting.')
def python_setup(init, build, yes):
    """Command-line interface for managing Python setup."""
    if init:
        initialize_setup(yes)
    elif build:
        build_package()
    else:
        click.echo("Please specify either --init or --build.")

def initialize_setup(yes):
    """Initialize the setup."""
    config = load_config()
    generator = SetupGenerator(config)
    click.echo(f"{Fore.CYAN}Welcome to the Setup.py Generator!{Style.RESET_ALL}")

    # If --yes is provided, set all defaults without prompting the user
    user_info = generator.prompt_for_info() if not yes else {}

    # Generate setup.py content
    setup_py_content = generator.generate_setup_py(user_info)

    # Save setup.py to file
    generator.save_setup_py(setup_py_content)

    click.echo(f"{Fore.GREEN}setup.py file generated successfully!{Style.RESET_ALL}")

def build_package():
    """Build the package using setuptools."""
    click.echo("Building the package...")  # Add your build logic here

if __name__ == "__main__":
    python_setup()
