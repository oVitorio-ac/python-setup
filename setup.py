
# setup.py
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

setup(
    name='python-setup',
    version='1.0.0',
    description='',
    author='Vitório A. Cavalheiro',
    author_email='vitoriocavalheiro03@gmail.com',
    long_description=README,
    packages=find_packages(),
    zip_safe=False
)
