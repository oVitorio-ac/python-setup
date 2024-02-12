# setup_generator.py
import click
import os
import subprocess
import json


class SetupGenerator:
    def __init__(self, config):
        self.config = config

    def get_git_info(self, info_type):
        try:
            result = subprocess.check_output(["git", "config",
                                                f"user.{info_type}"]).decode().strip()
            return result if result else None
        except subprocess.CalledProcessError:
            return None

    def prompt_for_info(self):
        prompts = self.config['prompts']
        user_info = {}

        # Obtém o nome da pasta como valor padrão para 'package name'
        default_package_name = os.path.basename(os.getcwd())

        for key, prompt_config in prompts.items():
            default_value = prompt_config.get('default', '')

            # Define o valor padrão para 'package name' como o nome da pasta
            if key == 'name' and not default_value:
                default_value = default_package_name

            # Obtém automaticamente o nome e o e-mail do git se não houver valor padrão
            if key == 'author' and not default_value:
                default_value = self.get_git_info('name')

            if key == 'author_email' and not default_value:
                default_value = self.get_git_info('email')

            prompt_text = prompt_config['text']

            # Ajuste para lidar melhor com listas nos valores padrão
            if isinstance(default_value, list):
                default_value = ', '.join(default_value)

            # Use click.style para aplicar cores diretamente aos valores
            styled_prompt_text = click.style(prompt_text, fg='cyan')
            styled_default_value = click.style(default_value, fg='green')

            # Atribua o resultado de click.style ou passe diretamente para click.prompt
            user_info[key] = click.prompt(f"{styled_prompt_text}",
                                            default=styled_default_value, type=click.UNPROCESSED)

            # Ajuste para lidar melhor com listas nas respostas
            if isinstance(user_info[key], str) and ',' in user_info[key]:
                user_info[key] = user_info[key].split(',')

        return user_info

    def generate_setup_py(self, user_info):
        """
        Generate a setup.py file content with the provided user_info.

        Parameters:
            self: The instance of the class.
            user_info (dict): A dictionary containing information for setup.py generation.

        Returns:
            str: The content of the setup.py file.
        """
        setup_py_content = f"""
        # setup.py
        import pathlib
        from setuptools import setup, find_packages

        HERE = pathlib.Path(__file__).parent
        README = (HERE / 'README.md').read_text()

        setup(
            name='{user_info['name']}',
            version='{user_info['version']}',
            description='{user_info['description']}',
            author='{user_info['author']}',
            author_email='{user_info['author_email']}',
            url='{user_info['url']}',
            license='{user_info['license']}',
            long_description=README,
            packages=find_packages(),
            install_requires={user_info['install_requires']},
            script_args={user_info['script_args']},
            zip_safe={user_info['zip_safe']}
        )
        """
        return setup_py_content

    def save_setup_py(self, setup_py_content, filename='setup.py'):
        """
        Write the setup.py content to a file.

        Args:
            setup_py_content (str): The content of the setup.py file.
            filename (str, optional): The name of the file to write to. Defaults to 'setup.py'.

        Returns:
            None
        """
        with open(filename, 'w', encoding="utf-8") as setup_file:
            setup_file.write(setup_py_content)


def load_config(config_path='setup_generator\config.json'):
    """
    Load the configuration from the specified path.

    :param config_path: The path to the configuration file (default is 'setup_generator\config.json').
    :return: The loaded configuration.
    """
    with open(config_path, 'r', encoding="utf-8") as config_file:
        return json.load(config_file)
