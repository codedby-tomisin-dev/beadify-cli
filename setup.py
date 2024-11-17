import os
from setuptools import setup, find_packages


# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


version = os.getenv("PACKAGE_VERSION", "0.0.1")


setup(
    name="beadify",
    version=version,
    description="A lightweight, efficient tool tailored for hobbyists looking to deploy multiple applications on a single Ubuntu-based VPS (Virtual Private Server)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tomisin Abiodun",
    author_email="decave.12357@gmail.com",
    url="https://github.com/CodeLexis/beadify-cli",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'click',
        'colorama',
        'paramiko',
        'pydantic',
    ],
    entry_points={
        "console_scripts": [
            "beadify=cli.__main__:cli"
        ]
    },
    package_data={
        "cli": ["scripts/*"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)