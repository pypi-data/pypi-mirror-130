#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `berhoel.helper`.
"""
from __future__ import division, print_function, absolute_import, unicode_literals

# Third party libraries.
import toml
import pytest

from berhoel import helper

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

__date__ = "2020/04/25 22:21:54 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"

  
@pytest.fixture
def base_path():
    return Path(__file__).parents[3]


@pytest.fixture
def py_project(base_path):
    return base_path / "pyproject.toml"


@pytest.fixture
def toml_inst(py_project):
    return toml.load(py_project.open("r"))


def test_version(toml_inst):
    assert helper.__version__ == toml_inst["tool"]["poetry"]["version"]


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
