from setuptools import setup, find_packages


setup(
    name="bead",
    version="1.0",
    description="A lightweight, efficient tool tailored for hobbyists looking to deploy multiple applications on a single Ubuntu-based VPS (Virtual Private Server)",
    author="Tomisin Abiodun",
    author_email="decave.12357@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        'click',
        'paramiko'
    ],
    entry_points={
        "console_scripts": [
            "bead=cli.__main__:cli"
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