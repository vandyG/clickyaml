from dataclasses import dataclass, field
from subprocess import Popen
from typing import Any
from typing import Callable
import click
from re import split


@dataclass()
class Commander:
    """Commander class takes in a parsed yaml and creates commands out of it.
    The *parsed_yaml* needs to be a dictionary of commands, and the *name* parameter
    is used to fetch the required information for the command.

    :param name: Name of the command to create. It's value is used to fetch the parameters
        out of the parsed yaml and is also used to create a command of the same *name*
    :type name: str
    :param parsed_yaml: Dictionary of commands, can include one or more commands.
    :type parsed_yaml: dict
    :param callback: Callback to be linked to the click Command.
    :type callback: Callable
    """

    name: str
    parsed_yaml: dict
    callback: Callable | None = field(repr=False,default=None)
    script: str = field(init=False, default="")
    _command: click.Command = field(init=False,repr=False)

    def __post_init__(self) -> None:
        self.parsed_yaml = self.parsed_yaml[self.name]
        self.script = self.parsed_yaml.pop("script") if "script" in self.parsed_yaml else ""
        self.callback = self.__default_callback__ if not self.callback else self.callback
        self._command = click.Command(name=self.name, callback=self.callback, **self.parsed_yaml)

    def __default_callback__(self, **kwargs) -> None:
        """The default callback assigned to the click command.
        """
        script_parms = split(r"(?<!\\)\s", self.script)
        params_in_order = [kwargs[key.lower()] for key in self.parsed_yaml["params"]]

        Popen(script_parms + params_in_order, text=True)

    @property
    def command(self):
        """The click Command created out of the yaml. Uses the default callback
        or the callback assigned to the commander object.

        :return: Click command created from the yaml file.
        :rtype: class: click.Command
        """
        self._command = click.Command(name=self.name, callback=self.callback, **self.parsed_yaml)
        return self._command
