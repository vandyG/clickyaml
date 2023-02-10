"""Main module."""

import os
from typing import Callable
from attr import dataclass, field
import yaml
import re
import sys
import click
from re import split

@dataclass
class Commander():
    parsed_yaml: dict = field(default=dict, repr=False)
    script: str = field(init=False)
    command: click.Command = field(init=False)
    _callback: Callable = field(init=False,repr=False)

    def __post__init__(self) -> None:
        ...

    def __default_callback__(self) -> None:
        ...

    def __run_script__(self, script) -> None:
        ...

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

    env_pattern = re.compile(".*?\\${(\\w+)}.*?")
    value = loader.construct_scalar(node)
    match = env_pattern.findall(str(value))  # to find all env variables in line

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

def construct_objects():
    pass

def parse_yaml(path=None, data=None) -> dict:

    loader = yaml.SafeLoader
    pass




# class Commander2:
#     def __init__(self, parsed_yaml) -> None:
#         self.parsed_yaml = parsed_yaml["commands"]

#     @classmethod
#     def create_commander(cls, path=None, data=None):
#         loader = yaml.SafeLoader

#         env_tag = "!ENV"
#         env_pattern = re.compile(".*?\\${(\\w+)}.*?")

#         def construct_env_vars(loader: yaml.Loader, node: yaml.Node):
#             """Extracts the environment variable from the node's value

#             :param loader: The yaml loader
#             :type loader: class: `yaml.Loader`
#             :param node: The current node in the yaml
#             :type node: class: `yaml.Node`S
#             :param pattern: The pattern in which to look for the environment variable .
#                 For ex. host: !ENV ${HOST}. The pattern here being `${ }`
#             :type pattern: class: `re.Pattern`
#             :return: a commander instance with the parsed string that contains the value of the environment
#                 variable
#             :rtype: class: `commander.Commander`
#             """
#             loader.add_implicit_resolver(env_tag, env_pattern, None)

#             value = loader.construct_scalar(node)
#             match = env_pattern.findall(value)  # to find all env variables in line

#             if match:
#                 full_value = value
#                 for g in match:
#                     full_value = full_value.replace(f"${{{g}}}", os.environ.get(g, g))

#                 return full_value
#             return value

#         def construct_arguments(loader: yaml.Loader, node: yaml.Node):
#             """Converts nodes with `!arg` tag to object of :class: `click.Argument`.
#             Passes the value associated with the node as arguments to the click.Argument constructor.

#             :param loader: The yaml loader
#             :type loader: class: `yaml.Loader`
#             :param node: The current node in the yaml
#             :type node: class: `yaml.Node`
#             :return: an instance of click Argument
#             :rtype: class: `click.Argument`
#             """
#             value = loader.construct_mapping(node, deep=True)
#             return click.Argument(**value)

#         def construct_options(loader: yaml.Loader, node: yaml.Node):
#             """Converts nodes with `!opt` tag to object of :class: `click.Option`.
#             Passes the value associated with the node as arguments to the click.Option constructor.

#             :param loader: The yaml loader
#             :type loader: class: `yaml.Loader`
#             :param node: The current node in the yaml
#             :type node: class: `yaml.Node`
#             :return: an instance of click Option
#             :rtype: class: `click.Option`
#             """
#             value = loader.construct_mapping(node, deep=True)
#             return click.Option(**value)

#         def construct_objects(loader: yaml.Loader, node: yaml.Node):
#             """Converts nodes with `!obj` tag to object of specified class.

#             :param loader: The yaml loader
#             :type loader: class: `yaml.Loader`
#             :param node: The current node in the yaml
#             :type node: class: `yaml.Node`
#             :return: returns an object of type defined in the yaml node
#             :rtype: `Any`
#             """
#             values = loader.construct_mapping(node)
#             mdl_cls = values.pop("class").split(".")
#             module = mdl_cls[0]
#             my_cls = mdl_cls[1]
#             return getattr(sys.modules[module], my_cls)(**values)

#         loader.add_constructor("!ENV", construct_env_vars)
#         loader.add_constructor("!obj", construct_objects)
#         loader.add_constructor("!arg", construct_arguments)
#         loader.add_constructor("!opt", construct_options)

#         if path:
#             with open(path) as conf_data:
#                 parsed_yaml = yaml.load(conf_data, Loader=loader)
#                 return cls(parsed_yaml)
#         elif data:
#             parsed_yaml = yaml.load(data, Loader=loader)
#             return cls(parsed_yaml)
#         else:
#             raise ValueError("Either a path or data should be defined as input")

#     def get_command(self, command_name, callback=None):
#         command_dict = self.parsed_yaml[command_name]

#         script = command_dict.pop("script") if "script" in command_dict else None

#         params_in_order = [value.human_readable_name for value in command_dict["params"]]

#         command = click.Command(
#             name=command_name, **self.parsed_yaml[command_name]
#         )

#         def default_callback(**kwargs):
#             from subprocess import Popen,run

#             args = [kwargs[key.lower()] for key in params_in_order]

#             scr = split(r"(?<!\\)\s", script)

#             Popen(scr + args, text=True)

#         if not callback:
#             command.callback = default_callback
#         else:
#             command.callback = callback

#         return (command, script)


if __name__ == "__main__":
    yaml_str = """
    commands:
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

    cmdr1 = Commander()
    cmdr2 = Commander()

    print(cmdr1.parsed_yaml)
    print(cmdr2.parsed_yaml)

    cmdr1.parsed_yaml = {"test": "test"}

    print(cmdr1.parsed_yaml)
    print(cmdr2.parsed_yaml)
    # cmdr = Commander.create_commander(data=yaml_str)
    # cmd, scr = cmdr.get_command("simplecommand")

    # runner = CliRunner()

    # result = runner.invoke(cmd,["arg1","arg2","--option=opt"])
    # print(result.output)
