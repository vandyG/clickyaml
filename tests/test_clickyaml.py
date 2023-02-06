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
        simplecommand:
            script: "/home/user/scripts/simplecommand.bash"
            params:
                - !arg
                    param_decls: [argument]
                - !opt
                    param_decls: ["--option"]

        complexcommand:
            script: "/home/user/scripts/complexcommand.bash"
            help: "Complex Command"
            params:
                - !arg
                    param_decls: [id]
                - !arg
                    param_decls: [type]
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
    assert "simplecommand" in cmdr.parsed_yaml
    assert "complexcommand" in cmdr.parsed_yaml
    assert "script" in cmdr.parsed_yaml["simplecommand"]
    assert "script" in cmdr.parsed_yaml["complexcommand"]
    assert "help" not in cmdr.parsed_yaml["simplecommand"]
    assert "help" in cmdr.parsed_yaml["complexcommand"]
    assert "params" in cmdr.parsed_yaml["simplecommand"]
    assert "params" in cmdr.parsed_yaml["complexcommand"]

def test_get_command(yaml_str):

    cmdr = commander.Commander.create_commander(data=yaml_str)

    command1, script1 = cmdr.get_command("simplecommand", lambda **kwargs : print("Simple Command"))
    command2, script2 = cmdr.get_command("complexcommand", lambda **kwargs : print("Complex Command"))
    assert "simplecommand" == command1.name
    assert "complexcommand" == command2.name
    assert "simplecommand.bash" in script1
    assert "complexcommand.bash" in script2

    runner = CliRunner()
    result = runner.invoke(command1, ["arg", "--option=opt"])
    assert "Simple" in result.output
    assert result.exit_code == 0

    result = runner.invoke(command2, ["id", "type", "all","--email=test@test.com"])
    assert "Complex" in result.output
    assert result.exit_code == 0
