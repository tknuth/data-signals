from setuptools import setup, find_packages

requires = ["pandas"]

dev_requires = ["bump2version", "pytest", "pytest-sugar", "seaborn"]

setup(
    name="Panda Detective",
    version="1.0.0",
    description="Utilities for pandas dataframes",
    author="Tobias Knuth",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requires,
    extras_require={"dev": dev_requires},
)
