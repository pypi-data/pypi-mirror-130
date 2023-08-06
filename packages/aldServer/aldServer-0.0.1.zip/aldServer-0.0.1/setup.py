from setuptools import setup, find_packages
from aldServer import __version__

setup(
    name = 'aldServer',
    author='Aldison Lluka', 
    author_email='aldison.lluka.al@gmail.com',
    description='aldServer - a template server',
    packages = find_packages(),
    python_requires='>=3',
    version = __version__
)