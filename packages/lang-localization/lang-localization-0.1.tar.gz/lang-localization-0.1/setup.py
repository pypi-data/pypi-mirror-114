from setuptools import setup, find_packages
import os

VERSION = '0.1'
DESCRIPTION = 'Translate your program'
LONG_DESCRIPTION = 'A package that allows to add different languages to your program.'

# Setting up
setup(
    name="lang-localization",
    version=VERSION,
    author="Patrik Ackermann",
    author_email="<patrik.ackermann@outlook.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'language', 'localize', 'translate'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
