import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '1.1.0'
PACKAGE_NAME = 'elemenpy'
AUTHOR = 'Eric Cheng'
AUTHOR_EMAIL = 'ericcheng9316@gmail.com'
URL = 'https://github.com/import-brain/elements.py'

LICENSE = 'MIT License'
DESCRIPTION = "A simple library for displaying an element's properties."
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'elements_py'
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
