"""Facilitates CLI commands
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
  name='micropython-ota-updater',
  version='1.0.0',
  python_requires='>=3.5, <4',
  install_requires=['rshell', 'esptool'],
)