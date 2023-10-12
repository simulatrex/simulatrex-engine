from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="simulatrex",
    version="0.0.1",
    author="Dominik Scherm",
    author_email="me@dominikscherm.de",
    description="LLM-based simulation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mypackage",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openai",
        "uuid",
        "numpy",
        "termcolor",
        "chromadb",
        "pydantic",
        "python-dotenv",
        "requests",
    ],
)
