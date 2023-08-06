import os

from setuptools import find_packages, setup

from httpx_caching import __version__

with open(os.path.join(os.getcwd(), "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="http-caching4",
    version=__version__,
    description="Caching support for Async httpx Client. Cloned from https://github.com/kovan/httpx-caching, https://github.com/johtso/httpx-caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ms280690/httpx-caching4.git",
    author="Mehul Solanki",
    author_email="ms280690@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "httpx==0.18.*",
        "msgpack",
        "anyio",
        "multimethod",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
            "pytest-mock",
            "pytest-timeout",
            "mock",
            "types-mock",
            "cherrypy",
            "freezegun",
            "types-freezegun",
            "autoflake",
            "black",
            "isort",
            "autoflake",
            "flake8",
            "flake8-bugbear",
            "mypy",
            "unasync",
            "types-dataclasses",
        ],
    },
    test_suite="tests",
    python_requires=">=3.8",
)