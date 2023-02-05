=========
clickYaml
=========


.. image:: https://img.shields.io/pypi/v/clickyaml.svg
        :target: https://pypi.python.org/pypi/clickyaml

.. image:: https://readthedocs.org/projects/clickyaml/badge/?version=latest
        :target: https://clickyaml.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/vandyG/clickyaml/shield.svg
     :target: https://pyup.io/repos/github/vandyG/clickyaml/
     :alt: Updates



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
                    param_decls: [option]

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




Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
