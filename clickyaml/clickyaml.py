"""Main module."""

import errno
from pathlib import Path
from typing import Any, Callable
from clickyaml.commander import Commander
import yaml
import re
import os
import click
import sys

ENV_PATTERN = re.compile(".*?\\${(\\w+)}.*?")


def construct_env_vars(loader: yaml.Loader, node: yaml.ScalarNode):
    """Extracts the environment variable from the node's value.

    :param loader: The yaml loader
    :type loader: yaml.Loader
    :param node: The current node in the yaml
    :type node: yaml.ScalarNode
    :return: A Scalar Node with the pattern replaced by environment variables
    :rtype: yaml.ScalarNode

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
    """Converts nodes with `!arg` tag to object of :py:class:`click.Argument`.

    Passes the value associated with the node as arguments to the click.Argument constructor.

    :param loader: The yaml loader
    :type loader: yaml.Loader
    :param node: The current node in the yaml
    :type node: yaml.Node
    :return: an instance of click Argument
    :rtype: click.Argument

    :Example:

    .. code-block:: yaml

        !arg
            param_decls: [category]

    This will be converted to ``click.Argument(param_decls = ["category"])``
    """

    value = loader.construct_mapping(node, deep=True)
    return click.Argument(**value)


def construct_options(loader: yaml.Loader, node: yaml.MappingNode):
    """Converts nodes with `!opt` tag to object of :py:class:`click.Option`.

    :param loader: The yaml loader
    :type loader: yaml.Loader
    :param node: The current node in the yaml
    :type node: yaml.Node
    :return: an instance of click Option
    :rtype: click.Option

    :Example:

    .. code-block:: yaml

        !opt
            param_decls: ["--type", "-t"]

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
    :type loader: yaml.Loader
    :param node: The current node in the yaml
    :type node: yaml.Node
    :return: returns an object of type defined in the yaml node
    :rtype: Any

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


def parse_yaml(path=None, data=None) -> dict:
    """Parses a yaml files and loads it into a python dictionary

    It can deal with 4 types of tags:
        - **!arg**: converts the yaml node to ``click.Argument`` object
        - **!opt**: converts the yaml node to ``click.Option`` object
        - **!obj**: converts the yaml node to the specified class object
        - **!env**: replaces the environment variables with the associated values

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


def get_command(name: str, parsed_yaml: dict, callback=None) -> click.Command:
    """Returns the desired command from the yaml file

    It has the ability to assign custom callbacks to the command. If a callback is
    not passed a default callback is assigned. The default callback runs the script
    associated with the command.

    .. seealso::

        The :ref:`callback <callback>` property of Commander class.

    :param name: Name of the command.
    :type name: str
    :param parsed_yaml: Dictionary from the parsed yaml of the command.
        Contains the parameters to be passed to the click constructor
    :type parsed_yaml: str
    :param callback: The callback to invoke on running the command, defaults to None
    :type callback: Callable | None, optional
    :return: The click command with desired parameters.
    :rtype: click.Command
    """

    cmdr = Commander(name=name, parsed_yaml=parsed_yaml[name])

    if callback:
        cmdr.callback = callback

    return cmdr.command


def get_commanders(yaml: str) -> dict:
    """Returns all the :py:class:`Commander <clickyaml.commander.Commander>` objects from the yaml data in a python dictionary

    :param yaml: The yaml data, this can be path to a file or a string
    :type yaml: str
    :return: A dictionary of Commander objects
    :rtype: dict[str, Commander]
    """

    try:
        is_file = Path(yaml).is_file()
    except OSError as oserror:
        if oserror.errno == errno.ENAMETOOLONG:
            is_file = False

    if is_file:
        parsed_yaml = parse_yaml(path=yaml)
    else:
        parsed_yaml = parse_yaml(data=yaml)

    commanders = {}

    for commander, params in parsed_yaml.items():
        cmdr = Commander(name=commander, parsed_yaml=params)
        commanders[commander] = cmdr

    return commanders
