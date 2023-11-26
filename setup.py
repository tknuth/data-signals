from setuptools import setup, find_packages

requires = ["pandas"]

dev_requires = ["bump2version", "pytest", "pytest-sugar", "seaborn"]

setup(
    name="Data Signals",
    version="1.0.0",
    description="Data signals offer a declarative approach to managing assumptions about data.",
    author="Tobias Knuth",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requires,
    extras_require={"dev": dev_requires},
)
