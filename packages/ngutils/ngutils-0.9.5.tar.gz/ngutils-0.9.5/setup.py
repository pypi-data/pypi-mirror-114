import pathlib
from setuptools import setup, find_packages

setup(
    name=find_packages()[0],
    version='0.9.5',
    author='nigani',
    author_email='nigani@internet.ru',
    description='Some useful ETL, EDA & other features',
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    license='GNU GPL v3',
    url='https://github.com/nigani/ngutils',
    install_requires=list(filter(None, pathlib.Path("requirements.txt").read_text().splitlines())),
    packages=find_packages()
)
