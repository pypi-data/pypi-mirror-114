from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="sssss",
    version="0.1.2",
    packages=["sssss",],
    install_requires=[],
    license="CC0",
    url="https://github.com/reity/sssss",
    author="Wyatt Howe",
    author_email="whowe@bu.edu",
    description="Static (version of) Shamir's Secret Sharing Scheme",
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
