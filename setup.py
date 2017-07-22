# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('diet/diet.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "cmdline-diet",
    packages = ["diet"],
    entry_points = {
        "console_scripts": ['diet = diet.diet:main']
        },
    version = version,
    description = "No description yet...",
    long_description = long_descr,
    author = "Vlad Stoian",
    author_email = "vstoian@pivotal.io",
    url = "https://github.com/vlad-stoian/diet",
    )

