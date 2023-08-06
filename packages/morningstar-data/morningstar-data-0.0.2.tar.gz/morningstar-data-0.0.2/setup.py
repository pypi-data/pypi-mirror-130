import setuptools
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="morningstar-data", 
    version="0.0.2",
    author="Morningstar",
    description="Package to interact with Morningstar Data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://developer.morningstar.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)