#!/usr/bin/env python

"""Tests for `clickyaml` package."""

import pytest

from click.testing import CliRunner

from clickyaml import commander

@pytest.fixture
def yaml_str():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    yaml_str = """
    commands:
        adhoc:
            script: "nohup /home/user/script/source/run_adhoc.scr"
            help: "Invokes an adhoc run for SAS ABPs. Requires three parameters ABP ID, Analytic Type and LOB/Platform. ABP ID should just be without the 'abp' prefix."
            params:
                - !arg
                    param_decls: [id]
                - !arg
                    param_decls: [type]
                    type: !obj
                        class: click.Choice
                        choices: ["a", "b"]
                        case_sensitive: False
                - !arg
                    param_decls: [category]
                    type: !obj
                        class: click.Choice
                        choices: ["1","2","3","ALL"]
                        case_sensitive: False
                - !opt
                    param_decls: ["--email","-E"]
                    multiple: True
                    envvar: MY_EMAIL
                    help: "Specify the mailing list with this option"
    """

    return yaml_str

    # return commander.Commander.create_commander('/mnt/c/Users/vgoel9/OneDrive - UHG/Rules/Special/clickyaml/tests/commands.yaml')



def test_content():
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_parse_yaml(yaml_str):
    """Test parse_pyaml"""
    # parsed = clickyaml.parse_yaml('/mnt/c/Users/vgoel9/OneDrive - UHG/Rules/Special/clickyaml/tests/commands.yaml')
    # assert "commands" in parsed.keys()
    # assert isinstance(parsed["commands"], dict)

    cmdr = commander.Commander.create_commander(data=yaml_str)

    assert all(isinstance(key, str) for key in cmdr.parsed_yaml.keys())
    assert all(isinstance(value, dict) for value in cmdr.parsed_yaml.values())
    assert "adhoc" in cmdr.parsed_yaml
    assert "script" in cmdr.parsed_yaml["adhoc"]
    assert "help" in cmdr.parsed_yaml["adhoc"]
    assert "params" in cmdr.parsed_yaml["adhoc"]

def test_get_command(yaml_str):

    cmdr = commander.Commander.create_commander(data=yaml_str)

    command, script = cmdr.get_command("adhoc", lambda id, type, category, email : print("hello"))
    assert "adhoc" == command.name
    assert "run_adhoc.scr" in script

    runner = CliRunner()
    result = runner.invoke(command, ["4402", "a","all"])
    assert "hello" in result.output
    assert result.exit_code == 0
