from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Print like someone is typing'
LONG_DESCRIPTION = 'A package that print provided string letter by letter'

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
]

# Setting up
setup(
    name="typeprint",
    version=VERSION,
    author="Atharva Bhandvalkar",
    author_email="<atharv.bhandvalkar@gmail.com>",
    license='MIT',
    url='https://github.com/a-tharva/type',
    description=DESCRIPTION,
    long_description=long_description + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=classifiers,
)