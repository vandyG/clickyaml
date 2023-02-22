from dataclasses import dataclass, field
from subprocess import Popen
from typing import Any
from typing import Callable
import click


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
    """

    name: str
    parsed_yaml: dict
    script: str = field(init=False, default="")
    _callback: Any = field(repr=False, default=None, init=False)
    _command: click.Command = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.script = self.parsed_yaml.get("script", "")
        self._callback = (
            self.__default_callback__ if not self._callback else self._callback
        )

        self.command_args = {
            key: self.parsed_yaml[key] for key in self.parsed_yaml.keys() - ["script"]
        }
        self._command = click.Command(
            name=self.name, callback=self._callback, **self.command_args
        )

    def __default_callback__(self, **kwargs) -> None:
        """The default callback assigned to the click command."""
        script_parms = self.script.split()
        params_in_order = [
            kwargs[value.human_readable_name.lower()]
            for value in self.parsed_yaml["params"]
        ]

        Popen(script_parms + params_in_order, text=True)

    @property
    def command(self):
        """The click Command created out of the yaml. Uses the default callback
        or the callback assigned to the commander object.

        :return: Click command created from the yaml file.
        :rtype: class: click.Command
        """
        self._command = click.Command(
            name=self.name, callback=self._callback, **self.command_args
        )
        return self._command

    @property
    def callback(self):
        """
        .. _callback:

        Callback to be linked to the click Command.

        If no callback is passed, the command is passed a default callback.
        The default callback runs the script associated with the command and
        passes the arguments in the order they are defined in the yaml file.

        :return: The callback linked to the click command
        :rtype: Callable
        """
        return self._callback

    @callback.setter
    def callback(self, value):
        if callable(value):
            self._callback = value
            self.command.callback = value
        else:
            raise TypeError("'value' needs to be a function/lambda")
