#!/usr/bin/env python

"""Tests for bad calls to deploy."""

import pytest
import mock
import os

from click.testing import CliRunner

from cloudformation_helper import cli
from cloudformation_helper.utils import aws

HERE = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(HERE, "..", "data", "config")


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=False)
def test_stack_wrong_name(mock_aws_stack_exists, mock_boto3):
    """Create a new stack"""
    runner = CliRunner()

    with pytest.raises(
        Exception, match=r"Could not find stack config named 'IamNotAStack'"
    ):
        runner.invoke(
            cli.cfhelper,
            [
                "--config",
                os.path.join(CONFIG_DIR, "valid_multistacks.cfh"),
                "deploy",
                "IamNotAStack",
            ],
            catch_exceptions=False,
        )


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=True)
def test_update_with_existing_changeset(
    mock_aws_has_changeset, mock_aws_stack_exists, mock_boto3
):
    """Try to update an existing changeset; but a changeset already exists, bail out"""
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
        input="n\n",
    )

    mock_boto3.client.return_value.create_change_set.assert_not_called()
    mock_boto3.client.return_value.execute_change_set.assert_not_called()


@mock.patch("cloudformation_helper.utils.aws.boto3")
@mock.patch.object(aws, "stack_exists", return_value=True)
@mock.patch.object(aws, "has_changeset", return_value=True)
def test_update_with_existing_changeset_and_continue(
    mock_aws_has_changeset, mock_aws_stack_exists, mock_boto3
):
    """Try to update an existing changeset; but a changeset already exists, delete it and continue"""
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
        input="y\ny\n",
    )

    mock_boto3.client.return_value.create_change_set.assert_called_once_with(
        StackName="MyStackName",
        TemplateBody=mock.ANY,
        Capabilities=mock.ANY,
        ChangeSetName=aws.CHANGESET_NAME,
        ChangeSetType="UPDATE",
    )

    mock_boto3.client.return_value.delete_change_set.assert_called_once_with(
        StackName="MyStackName", ChangeSetName=aws.CHANGESET_NAME
    )
    mock_boto3.client.return_value.execute_change_set.assert_called_once_with(
        StackName="MyStackName", ChangeSetName=aws.CHANGESET_NAME
    )
