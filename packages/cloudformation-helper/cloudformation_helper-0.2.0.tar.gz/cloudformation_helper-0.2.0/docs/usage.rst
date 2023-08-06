=====
Usage
=====

This project is not structured as a library per say. There is no easy way to use it programmatically.

Installing it will expose a script called `cfhelper`. It relies on a configuration file that describes your stacks.

Sample `stacks.cfh` file:

.. code-block:: yaml

  # CloudFormation-helper config

  MyStackAlias:
    stack: MyStackName
    file: myStackFile.yml
    use_changesets: false

Once you have the above configuration file, you can deploy the stack by running `cfhelper deploy MyStackAlias`. You can
also specify the configuration file to use either through a flag, `cfhelper --config ../path/to/config.cfh deploy MyStackAlias`,
or through an environment variable `CFHELPER_CONFIG=../path/to/config.cfh cfhelper deploy MyStackAlias`.

The file attribute of your stack will be searched relative to the configuration file.
