#!/usr/bin/env python

"""Tests for `ecs_composex_specs` package."""

from json import loads
from os import path

import jsonschema
import yaml
from importlib_resources import files
from yaml import Loader


def test_valid_schema():
    """
    Function to test valid schema
    :return:
    """

    with open(
        f"{path.abspath(path.dirname(__file__))}/blog.features.yml", "r"
    ) as content_fd:
        content = yaml.load(content_fd.read(), Loader=Loader)
    source = files("ecs_composex_specs").joinpath("compose-spec.json")
    resolver = jsonschema.RefResolver(
        f"file://{path.abspath(path.dirname(source))}/", None
    )
    jsonschema.validate(
        content,
        loads(source.read_text()),
        resolver=resolver,
    )
