import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.8'
PACKAGE_NAME = 'ngutils'
AUTHOR = 'nugani'
AUTHOR_EMAIL = 'ganibaev@gmail.com'
URL = 'https://github.com/nigani'

LICENSE = 'Apache License 2.0'
DESCRIPTION = 'Tools for DataScience'
LONG_DESCRIPTION = (HERE / "readme.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
'pandas',
'requests'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )