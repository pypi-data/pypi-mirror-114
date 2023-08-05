"""Setup script for realpython-reader"""

import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

NAME = "mltrackingclient"
VERSION = "1.0.1"

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name=NAME,
    version=VERSION,
    description="REST ML-AI API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/EimantasN/Equusight_BackEnd",
    author="Eimantas Noreika",
    author_email="noreika.eimantas@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "feedparser", "html2text", "importlib_resources", "typing"
    ],
    entry_points={"console_scripts": ["realpython=reader.__main__:main"]},
)
