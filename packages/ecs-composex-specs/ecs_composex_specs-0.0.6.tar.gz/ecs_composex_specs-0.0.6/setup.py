#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = []

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="John Preston",
    author_email="john@compose-x.io",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Specifications for ECS Compose-X",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords="ecs_composex_specs",
    name="ecs_composex_specs",
    packages=find_packages(include=["ecs_composex_specs", "ecs_composex_specs.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/johnpreston/ecs_composex_specs",
    version="0.0.6",
    zip_safe=False,
)
