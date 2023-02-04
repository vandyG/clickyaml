"""Main module."""

import yaml
import re
import sys
import click

def parse_yaml(path=None, data=None):

    loader = yaml.SafeLoader

    env_tag = "!ENV"
    env_pattern = re.compile(".*?\${(\w+)}.*?")

    def construct_env_vars(loader: yaml.Loader, node: yaml.Node):
        """Extracts the environment variable from the node's value

        :param loader: The yaml loader
        :type loader: class: `yaml.Loader`
        :param node: The current node in the yaml
        :type node: class: `yaml.Node`S
        :param pattern: The pattern in which to look for the environment variable .
            For ex. host: !ENV ${HOST}. The pattern here being `${ }`
        :type pattern: class: `re.Pattern`
        :return: the parsed string that contains the value of the environment
            variable
        :rtype: `str`
        """
        loader.add_implicit_resolver(env_tag, env_pattern, None)

        value = loader.construct_scalar(node)
        match = env_pattern.findall(value)  # to find all env variables in line

        if match:
            full_value = value
            for g in match:
                full_value = full_value.replace(f"${{{g}}}", os.environ.get(g, g))

            return full_value
        return value

    def construct_arguments(loader: yaml.Loader, node: yaml.Node):
        """Converts nodes with `!arg` tag to object of :class: `click.Argument`.
        Passes the value associated with the node as arguments to the click.Argument constructor.

        :param loader: The yaml loader
        :type loader: class: `yaml.Loader`
        :param node: The current node in the yaml
        :type node: class: `yaml.Node`
        :return: an instance of click Argument
        :rtype: class: `click.Argument`
        """
        value = loader.construct_mapping(node, deep=True)
        return click.Argument(**value)

    def construct_options(loader: yaml.Loader, node: yaml.Node):
        """Converts nodes with `!opt` tag to object of :class: `click.Option`.
        Passes the value associated with the node as arguments to the click.Option constructor.

        :param loader: The yaml loader
        :type loader: class: `yaml.Loader`
        :param node: The current node in the yaml
        :type node: class: `yaml.Node`
        :return: an instance of click Option
        :rtype: class: `click.Option`
        """
        value = loader.construct_mapping(node, deep=True)
        return click.Option(**value)

    def construct_objects(loader: yaml.Loader, node: yaml.Node):
        """Converts nodes with `!obj` tag to object of specified class.

        :param loader: The yaml loader
        :type loader: class: `yaml.Loader`
        :param node: The current node in the yaml
        :type node: class: `yaml.Node`
        :return: returns an object of type defined in the yaml node
        :rtype: `Any`
        """
        values = loader.construct_mapping(node)
        mdl_cls = values.pop("class").split(".")
        module = mdl_cls[0]
        cls = mdl_cls[1]
        return getattr(sys.modules[module], cls)(**values)

    loader.add_constructor("!ENV", construct_env_vars)
    loader.add_constructor("!obj", construct_objects)
    loader.add_constructor("!arg", construct_arguments)
    loader.add_constructor("!opt", construct_options)

    if path:
        with open(path) as conf_data:
            return yaml.load(conf_data, Loader=loader)
    elif data:
        return yaml.load(data, Loader=loader)
    else:
        raise ValueError("Either a path or data should be defined as input")

