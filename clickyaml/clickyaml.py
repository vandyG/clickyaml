"""Main module."""

import pathlib
from typing import Any
from clickyaml.commander import Commander
import yaml
import re
import os
import click
import sys

ENV_PATTERN = re.compile(".*?\\${(\\w+)}.*?")


def construct_env_vars(loader: yaml.Loader, node: yaml.ScalarNode):
    """Extracts the environment variable from the node's value

    :param loader: The yaml loader
    :type loader: class: `yaml.Loader`
    :param node: The current node in the yaml
    :type node: class: `yaml.Node`
    :param pattern: Pattern for string env vars.
    :type pattern: class: `re.Pattern`
    :return: A Scalar Node with the pattern replaced by environment variables
    :rtype: class: `yaml.ScalarNode`

    :Example:
    For a node ``host: !ENV ${HOST}`` replaces the ``${ ... }`` with the value
    stored in the environment variable `HOST`

    """

    value = loader.construct_scalar(node)
    match = ENV_PATTERN.findall(str(value))  # to find all env variables in line

    if match:
        full_value = str(value)
        for g in match:
            full_value = full_value.replace(f"${{{g}}}", os.environ.get(g, g))

        return full_value

    return value


def construct_arguments(loader: yaml.Loader, node: yaml.MappingNode):
    """Converts nodes with `!arg` tag to object of :class: `click.Argument`.

    Passes the value associated with the node as arguments to the click.Argument constructor.

    :param loader: The yaml loader
    :type loader: class: `yaml.Loader`
    :param node: The current node in the yaml
    :type node: class: `yaml.Node`
    :return: an instance of click Argument
    :rtype: class: `click.Argument`

    :Example:
    .. code-block:: yaml

        !arg
            param_decls: [category]

    This will be converted to ``click.Argument(param_decls = ["category"])``
    """

    value = loader.construct_mapping(node, deep=True)
    return click.Argument(**value)


def construct_options(loader: yaml.Loader, node: yaml.MappingNode):
    """Converts nodes with `!opt` tag to object of :class: `click.Option`.

    Passes the value associated with the node as arguments to the click.Option constructor.

    :param loader: The yaml loader
    :type loader: class: `yaml.Loader`
    :param node: The current node in the yaml
    :type node: class: `yaml.Node`
    :return: an instance of click Option
    :rtype: class: `click.Option`

    :Example:
    .. code-block:: yaml

        !opt
            param_decls: ["--type","-t"]

    This will be converted to ``click.Option(param_decls = ["--type","-t"])``

    """

    value = loader.construct_mapping(node, deep=True)
    return click.Option(**value)


def construct_objects(loader: yaml.Loader, node: yaml.MappingNode):
    """Converts nodes with `!obj` tag to object of specified class.

    The yaml node needs to specified with the tag `!obj`. The first node should have key as *class* and
    the value should have the class object you want to create. Rest of the nodes are passed as parameters
    to the object at runtime.

    :param loader: The yaml loader
    :type loader: class: `yaml.Loader`
    :param node: The current node in the yaml
    :type node: class: `yaml.Node`
    :return: returns an object of type defined in the yaml node
    :rtype: `Any`

    :Example:
    .. code-block:: yaml

        type: !obj
            class: click.Choice
            choices: ["1","2","3","ALL"]
            case_sensitive: False

    This will be converted to ``click.Choice(choices = ["1","2","3","ALL"], case_sensitive = False)``
    """
    values = loader.construct_mapping(node)
    mdl_cls = values.pop("class").split(".")
    module = mdl_cls[0]
    my_cls = mdl_cls[1]

    return getattr(sys.modules[module], my_cls)(**values)


def parse_yaml(
    path: str | pathlib.Path | None = None, data: str | None = None
) -> dict[str, dict]:
    """Parses a yaml files and loads it into a python dictionary

    It can deal with 4 types of tags:
        - **!arg**: converts the yaml node to ``click.Argument`` object
        - **!opt**: converts the yaml node to ``click.Option`` object
        - **!obj**: converts the yaml node to the specified class object
        - **!env**: replaces the environment variables with the associated values.

    :param path: Defines the path to the yaml file that needs to be parsed, defaults to None
    :type path: str | pathlib.Path | None, optional
    :param data: The yaml data itself as a stream , defaults to None
    :type data: str | None, optional
    :raises ValueError: Raises the error if neither a path or data is defined as input
    :return: The parsed yaml file
    :rtype: dict[str, dict]
    """

    loader = yaml.SafeLoader

    loader.add_constructor("!ENV", construct_env_vars)
    loader.add_constructor("!obj", construct_objects)
    loader.add_constructor("!arg", construct_arguments)
    loader.add_constructor("!opt", construct_options)

    loader.add_implicit_resolver("!ENV", ENV_PATTERN, None)

    if path:
        with open(path) as conf_data:
            return yaml.load(conf_data, Loader=loader)
    elif data:
        return yaml.load(data, Loader=loader)
    else:
        raise ValueError("Either a path or data should be defined as input")


if __name__ == "__main__":
    yaml_str = """
    simplecommand:
        script: "nohup /mnt/c/Users/vgoel9/OneDrive\ -\ UHG/Rules/temp/scripts/simplecommand.bash"
        params:
            - !arg
                param_decls: [argument]
            - !opt
                param_decls: ["--option"]
            - !arg
                param_decls: ["argument2"]

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

    import re
    from click.testing import CliRunner

    # cmdr1 = Commander()
    # cmdr2 = Commander()

    # print(cmdr1.parsed_yaml)
    # print(cmdr2.parsed_yaml)

    # cmdr1.parsed_yaml = {"test": "test"}

    # print(cmdr1.parsed_yaml)
    # print(cmdr2.parsed_yaml)
    # cmdr = Commander.create_commander(data=yaml_str)
    # cmd, scr = cmdr.get_command("simplecommand")

    # runner = CliRunner()

    # result = runner.invoke(cmd,["arg1","arg2","--option=opt"])
    # print(result.output)
    from commander import Commander

    yml = parse_yaml(data=yaml_str)
    print(yml)
    print(type(yml))
    print(set(type(key) for key in yml.keys()))
    print(set(type(value) for value in yml.values()))

    cmdr = Commander(name="simplecommand",parsed_yaml = yml["simplecommand"])
    print(cmdr)
