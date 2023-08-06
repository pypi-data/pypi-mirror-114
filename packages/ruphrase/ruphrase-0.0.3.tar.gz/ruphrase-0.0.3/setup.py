import pathlib
from ruphrase import __version__ as ruphrase_version
from setuptools import setup, find_packages

setup(
    name=find_packages()[0],
    version=ruphrase_version,
    author='nigani',
    author_email='nigani@internet.ru',
    description='Build the correct turn of phrase in Russian',
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    license='MIT License',
    url='https://github.com/nigani/ruphrase',
    install_requires=list(filter(None, pathlib.Path("requirements.txt").read_text().splitlines())),
    packages=find_packages()
)
