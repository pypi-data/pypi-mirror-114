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


def test_x_efs_create():
    """
    Function to test valid schema
    :return:
    """

    with open(
        f"{path.abspath(path.dirname(__file__))}/x_efs/create.yml", "r"
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
