from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, "README.md")) as file:
        long_description = file.read()
else:
    with open(os.path.join(_here, "README.md"), encoding="utf-8") as file:
        long_description = file.read()

version = {}
with open(os.path.join(_here, "wanakana", "version.py")) as file:
    exec(file.read(), version)

setup(
    name="wanakana-python",
    version=version["__version__"],
    description=("Show how to structure a Python project."),
    long_description=long_description,
    author="starwort",
    url="https://github.com/starwort/wanakana",
    license="MPL-2.0",
    packages=["wanakana"],
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3.6"],
)

