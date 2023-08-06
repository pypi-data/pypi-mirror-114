#!/usr/bin/env python

"""Tests for `ecs_composex_specs` package."""

from os import path
import pytest
import yaml
from yaml import Loader
from importlib_resources import files
import jsonschema
from json import loads

from ecs_composex_specs import ecs_composex_specs


def test_x_vpc_lookup():
    """
    Function to test valid schema
    :return:
    """

    with open(
        f"{path.abspath(path.dirname(__file__))}/x_vpc/lookup.yml", "r"
    ) as content_fd:
        content = yaml.load(content_fd.read(), Loader=Loader)
    print(content)

    source = files("ecs_composex_specs").joinpath("x-vpc.spec.json")
    print(source)
    resolver = jsonschema.RefResolver(
        f"file://{path.abspath(path.dirname(source))}/", None
    )
    jsonschema.validate(
        content["x-vpc"],
        loads(source.read_text()),
        resolver=resolver,
    )


def test_x_vpc_lookup_invalid():
    """
    Function to test valid schema
    :return:
    """

    with open(
        f"{path.abspath(path.dirname(__file__))}/x_vpc/invalid_lookup.yml", "r"
    ) as content_fd:
        content = yaml.load(content_fd.read(), Loader=Loader)
    print(content)

    source = files("ecs_composex_specs").joinpath("x-vpc.spec.json")
    print(source)
    resolver = jsonschema.RefResolver(
        f"file://{path.abspath(path.dirname(source))}/", None
    )
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(
            content["x-vpc"],
            loads(source.read_text()),
            resolver=resolver,
        )


def test_x_vpc_create():
    """
    Function to test valid schema
    :return:
    """

    with open(
        f"{path.abspath(path.dirname(__file__))}/x_vpc/create.yml", "r"
    ) as content_fd:
        content = yaml.load(content_fd.read(), Loader=Loader)

    source = files("ecs_composex_specs").joinpath("x-vpc.spec.json")
    resolver = jsonschema.RefResolver(
        f"file://{path.abspath(path.dirname(source))}/", None
    )
    jsonschema.validate(
        content["x-vpc"],
        loads(source.read_text()),
        resolver=resolver,
    )


def test_x_vpc_use():
    """
    Function to test valid schema
    :return:
    """

    with open(
        f"{path.abspath(path.dirname(__file__))}/x_vpc/use.yml", "r"
    ) as content_fd:
        content = yaml.load(content_fd.read(), Loader=Loader)

    source = files("ecs_composex_specs").joinpath("x-vpc.spec.json")
    resolver = jsonschema.RefResolver(
        f"file://{path.abspath(path.dirname(source))}/", None
    )
    jsonschema.validate(
        content["x-vpc"],
        loads(source.read_text()),
        resolver=resolver,
    )
