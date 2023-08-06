#!/usr/bin/env python

"""Tests for valid calls to deploy."""

import mock
import os

from click.testing import CliRunner

from cloudformation_helper import cli
from cloudformation_helper.utils import aws

HERE = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(HERE, "..", "data", "config")


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=False)
def test_create(mock_aws_stack_exists, mock_boto3):
    """Create a new stack"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
    )
    mock_boto3.client.return_value.create_stack.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=[],
    )


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=True)
def test_update(mock_aws_stack_exists, mock_boto3):
    """Update an existing stack"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
    )
    mock_boto3.client.return_value.update_stack.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=[],
    )


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=False)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_create_with_changeset(
    mock_aws_has_changeset, mock_aws_stack_exists, mock_boto3
):
    """Create a new stack using changesets"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
        input="y\n",
    )

    mock_boto3.client.return_value.create_change_set.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=[],
        ChangeSetName=aws.CHANGESET_NAME,
        ChangeSetType="CREATE",
    )

    mock_boto3.client.return_value.execute_change_set.assert_called_once_with(
        StackName="MyStackName",
        ChangeSetName=aws.CHANGESET_NAME,
    )


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=False)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_create_with_changeset_no_execute(
    mock_aws_has_changeset, mock_aws_stack_exists, mock_boto3
):
    """Create a new stack using changesets, but don't execute"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
        input="n\ny\n",
    )

    mock_boto3.client.return_value.create_change_set.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=[],
        ChangeSetName=aws.CHANGESET_NAME,
        ChangeSetType="CREATE",
    )

    mock_boto3.client.return_value.execute_change_set.assert_not_called()
    mock_boto3.client.return_value.delete_change_set.assert_not_called()


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=False)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_create_with_changeset_no_execute_cleanup(
    mock_aws_has_changeset, mock_aws_stack_exists, mock_boto3
):
    """Create a new stack using changesets, don't execute and delete changeset"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
        input="n\nn\n",
    )

    mock_boto3.client.return_value.create_change_set.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=[],
        ChangeSetName=aws.CHANGESET_NAME,
        ChangeSetType="CREATE",
    )

    mock_boto3.client.return_value.execute_change_set.assert_not_called()
    mock_boto3.client.return_value.delete_change_set.assert_called_once_with(
        StackName="MyStackName",
        ChangeSetName=aws.CHANGESET_NAME,
    )


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_update_with_changeset(
    mock_aws_has_changeset, mock_aws_stack_exists, mock_boto3
):
    """Update an existing stack using changesets"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
        input="y\n",
    )

    mock_boto3.client.return_value.create_change_set.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=[],
        ChangeSetName=aws.CHANGESET_NAME,
        ChangeSetType="UPDATE",
    )

    mock_boto3.client.return_value.execute_change_set.assert_called_once_with(
        StackName="MyStackName",
        ChangeSetName=aws.CHANGESET_NAME,
    )


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_update_with_changeset_no_execute(
    mock_aws_has_changeset, mock_aws_stack_exists, mock_boto3
):
    """Update an existing stack using changesets but don't execute"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
        input="n\ny\n",
    )

    mock_boto3.client.return_value.create_change_set.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=[],
        ChangeSetName=aws.CHANGESET_NAME,
        ChangeSetType="UPDATE",
    )

    mock_boto3.client.return_value.execute_change_set.assert_not_called()
    mock_boto3.client.return_value.delete_change_set.assert_not_called()


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_update_with_changeset_no_execute_cleanup(
    mock_aws_has_changeset, mock_aws_stack_exists, mock_boto3
):
    """Update an existing stack using changesets, don't execute but delete changeset"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_with_changeset.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
        input="n\nn\n",
    )

    mock_boto3.client.return_value.create_change_set.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=[],
        ChangeSetName=aws.CHANGESET_NAME,
        ChangeSetType="UPDATE",
    )

    mock_boto3.client.return_value.execute_change_set.assert_not_called()
    mock_boto3.client.return_value.delete_change_set.assert_called_once_with(
        StackName="MyStackName",
        ChangeSetName=aws.CHANGESET_NAME,
    )


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=False)
def test_create_with_capabilities(mock_aws_stack_exists, mock_boto3):
    """Create a new stack"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(
                CONFIG_DIR, "valid_singlestack_with_multiple_capabilities.cfh"
            ),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
    )

    mock_boto3.client.return_value.create_stack.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
    )


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=True)
def test_update_with_capabilities(mock_aws_stack_exists, mock_boto3):
    """Update an existing stack"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(
                CONFIG_DIR, "valid_singlestack_with_multiple_capabilities.cfh"
            ),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
    )

    mock_boto3.client.return_value.update_stack.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
    )


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=False)
@mock.patch.object(aws, "has_changeset", return_value=False)
def test_create_with_changeset_and_capabilities(
    mock_aws_has_changeset, mock_aws_stack_exists, mock_boto3
):
    """Create a new stack using changesets"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(
                CONFIG_DIR, "valid_singlestack_capabilities_and_changeset.cfh"
            ),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
        input="y\n",
    )

    mock_boto3.client.return_value.create_change_set.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=["CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"],
        ChangeSetName=aws.CHANGESET_NAME,
        ChangeSetType="CREATE",
    )

    mock_boto3.client.return_value.execute_change_set.assert_called_once_with(
        StackName="MyStackName",
        ChangeSetName=aws.CHANGESET_NAME,
    )
