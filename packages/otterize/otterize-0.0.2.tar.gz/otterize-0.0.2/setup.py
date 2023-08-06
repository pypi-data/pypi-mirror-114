"""Setup script"""

import os.path
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="otterize",
    version="0.0.2",
    author="Otterize",
    author_email="pypi@otterize.com",
    url="https://otterize.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["otterize"],
    include_package_data=True,
)
