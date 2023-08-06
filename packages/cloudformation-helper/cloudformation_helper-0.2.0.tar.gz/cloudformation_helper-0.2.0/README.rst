=====================
cloudformation-helper
=====================


.. image:: https://img.shields.io/pypi/v/cloudformation_helper.svg
        :target: https://pypi.python.org/pypi/cloudformation_helper

.. image:: https://readthedocs.org/projects/cloudformation-helper/badge/?version=latest
        :target: https://cloudformation-helper.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


Small tool to simplify usage of CloudFormation. Wraps around a bit of configuration, changesets and abstracts
create vs update of a stack.

* Free software: MIT license
* Documentation: https://cloudformation-helper.readthedocs.io.


Usage
-----

.. code-block:: bash

   pip install cloudformation-helper
   vim stacks.cfh
   cfhelper deploy MyStackAlias


Sample `stacks.cfh` file:

.. code-block:: yaml

  MyStackAlias:
    stack: MyStackName
    file: myStackFile.yml
    use_changesets: false
    capabilities:
    - CAPABILITY_IAM
    - CAPABILITY_NAMED_IAM


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
