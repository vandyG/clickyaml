=========
clickYaml
=========


.. image:: https://img.shields.io/pypi/v/clickyaml.svg
        :target: https://pypi.python.org/pypi/clickyaml

.. image:: https://readthedocs.org/projects/clickyaml/badge/?version=latest
        :target: https://clickyaml.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://github.com/vandyG/clickyaml/actions/workflows/python-package.yml/badge.svg?event=push&branch=redesign
        :target: https://github.com/vandyG/clickyaml/actions/workflows/python-package.yml/badge.svg


ClickYaml reads a `.yaml` file and creates click Commands out of it.


* Free software: MIT license
* Documentation: https://clickyaml.readthedocs.io.

Installation
------------
To install clickYaml, run this command in your terminal:

.. code-block:: bash

    pip install clickyaml

Usage
--------

Input ``yaml`` file example:

.. code-block:: yaml

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

**Note**: There are certain rules on the structure of the yaml file:

- The root block needs to be named ``commands``.
- The commands block should contain other blocks which represents each command.
- Each command block needs to have blocks for each *parameter* of the command that you define. To know the available parameters refer to the `click documentation <https://click.palletsprojects.com/en/8.1.x/api/#click.Command>`_
- Apart from parameters to click.Command a *script* block can also be used. Script represents a script that you want to link with your command.
- There are three types of tags that can be used in the yaml file: `!obj`, `!arg` and `!opt`
- **!obj** can be used to create custom objects
- **!arg** can be used to create ``click.Argument`` objects
- **!opt** can be used to create ``click.Option`` objects

Converting the yaml data to ``click.Command`` using the ``Commander`` object

.. code-block:: python

    from clickyaml import Commander

    commander = Commander.create_commander(path=yaml_str)
    # pass any callback(function) that takes in all the Arguments and Options of the command
    # as parameters.
    simplecmd = commander.get_command("simplecommand", lambda **kwargs: print("Simple Command"))


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
