#!/usr/bin/env python

"""Tests for `clickyaml` package."""

import pytest

from click.testing import CliRunner

from clickyaml import commander, clickyaml

@pytest.fixture
def yaml_str():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    yaml_str = """
    simplecommand:
        script: "echo $1;echo $2"
        params:
            - !arg
                param_decls: [argument]
            - !opt
                param_decls: ["--option"]

    complexcommand:
        script: "echo$1;echo$2;echo$3;echo$4"
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

    parsed_yaml = clickyaml.parse_yaml(data=yaml_str)
    assert "simplecommand" in parsed_yaml.keys() and "complexcommand" in parsed_yaml.keys()

    assert "script" in parsed_yaml["simplecommand"].keys() and "params" in parsed_yaml["simplecommand"].keys()
    assert "script" in parsed_yaml["complexcommand"].keys() and "params" in parsed_yaml["complexcommand"].keys() and "help" in parsed_yaml["complexcommand"].keys()

    simp_params = list(parsed_yaml["simplecommand"]["params"])
    simp_param_count = len(simp_params)

    comp_params = list(parsed_yaml["complexcommand"]["params"])
    comp_params_count = len(comp_params)

    assert simp_param_count == 2
    assert comp_params_count == 4


def test_get_command(yaml_str):

    parsed = clickyaml.parse_yaml(data=yaml_str)
    simp = clickyaml.get_command("simplecommand",parsed_yaml=parsed, callback=lambda **kwargs: print(kwargs))
    comp = clickyaml.get_command("complexcommand",parsed_yaml=parsed,callback=lambda **kwargs: print(kwargs))

    runner = CliRunner()

    result = runner.invoke(simp, ["arg", "--option=opt"])
    assert "arg" in result.output
    assert "opt" in result.output
    assert result.exit_code == 0

    result = runner.invoke(comp, ["id", "type", "all","--email=test@test.com"])
    assert "id" in result.output
    assert "type" in result.output
    assert "ALL" in result.output
    assert "test@test.com" in result.output
    assert result.exit_code == 0


def test_get_commanders(yaml_str):

    commands = clickyaml.get_commanders(yaml_str)

    simp = commands["simplecommand"]
    comp = commands["complexcommand"]

    simp.callback = lambda **kwargs: print(kwargs)
    comp.callback = lambda **kwargs: print(kwargs)

    runner = CliRunner()

    result = runner.invoke(simp.command, ["arg", "--option=opt"])
    assert "arg" in result.output
    assert "opt" in result.output
    assert result.exit_code == 0

    result = runner.invoke(comp.command, ["id", "type", "all","--email=test@test.com"])
    assert "id" in result.output
    assert "type" in result.output
    assert "ALL" in result.output
    assert "test@test.com" in result.output
    assert result.exit_code == 0

def main():

    yaml = """
    simplecommand:
        script: "echo $1;echo $2"
        params:
            - !arg
                param_decls: [argument]
            - !opt
                param_decls: ["--option"]
    """

    commands = clickyaml.get_commands(yaml)

    simp = commands["simplecommand"]
    runner = CliRunner()
    result = runner.invoke(simp, ["arg", "--option=opt"])
    result2 = runner.invoke(simp, ["--help"])
    print(result.output)
    print(result2.output)

if __name__ == "__main__":
    main()
