#!/usr/bin/env python

"""Tests for `clickyaml` package."""

import pytest

from click.testing import CliRunner

from clickyaml import clickyaml, commander
from clickyaml import cli


@pytest.fixture
def cmdr():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """

    return commander.Commander.create_commander('/mnt/c/Users/vgoel9/OneDrive - UHG/Rules/Special/clickyaml/tests/commands.yaml')



def test_content():
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'clickyaml.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

def test_parse_yaml(cmdr):
    """Test parse_pyaml"""
    # parsed = clickyaml.parse_yaml('/mnt/c/Users/vgoel9/OneDrive - UHG/Rules/Special/clickyaml/tests/commands.yaml')
    # assert "commands" in parsed.keys()
    # assert isinstance(parsed["commands"], dict)

    assert all(isinstance(key, str) for key in cmdr.parsed_yaml.keys())
    assert all(isinstance(value, dict) for value in cmdr.parsed_yaml.values())
    assert "adhoc" in cmdr.parsed_yaml
    assert "script" in cmdr.parsed_yaml["adhoc"]
    assert "help" in cmdr.parsed_yaml["adhoc"]
    assert "params" in cmdr.parsed_yaml["adhoc"]

def test_get_command(cmdr):

    command, script = cmdr.get_command("adhoc", lambda abp, analytictype, lobplat, email, runtype : print("hello"))
    assert "adhoc" == command.name
    assert "run_adhoc.scr" in script

    runner = CliRunner()
    result = runner.invoke(command, ["4402", "prof","unet"])
    assert "hello" in result.output
    assert result.exit_code == 0
