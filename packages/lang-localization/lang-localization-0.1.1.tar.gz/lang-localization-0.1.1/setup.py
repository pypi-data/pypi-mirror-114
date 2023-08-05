from setuptools import setup, find_packages
import os

VERSION = '0.1.1'
DESCRIPTION = 'Translate your program'
LONG_DESCRIPTION = '#lang-localization\nWith lang-localization you can translate your program to different languages.\nIt is not possible translating your program easier.\n\n## How to use\nStart by creating a folder named "localization" in the directory where your python file is located. For every language you want to add you need to create a file with the .loc ending in the new directory. For example "de.loc" or "en.loc". \nThe inside of the file must look like this:\n```\nhw = Hello World!\nbutton1 = Press Me\n``` \nYour python file must look like this:\n```python\nimport localization\n\nlocalization.setLang("de") # The string must be the same as the filename of your translation without .loc\n\nprint(localization.get("hw"))\n\nrandomButtonCreateFunction(text=localization.get("button1"))\n```'

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
