#!/usr/bin/env python

"""Tests for `cloudformation_helper` config management."""

import mock
import os
import pytest
import yaml

from click.testing import CliRunner

from cloudformation_helper import cli
from cloudformation_helper.commands import deploy

HERE = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIR = os.path.join(HERE, "data", "config")


def test_config_file_does_not_exist():
    """Pass a file path that does not exist"""
    runner = CliRunner()
    with pytest.raises(FileNotFoundError, match=r"No such file or directory"):
        runner.invoke(
            cli.cfhelper,
            ["--config", "not-a-valid-file", "deploy"],
            catch_exceptions=False,
        )


def test_wrong_config_format():
    """Pass a file that has the wrong format"""
    runner = CliRunner()
    with pytest.raises(yaml.parser.ParserError):
        runner.invoke(
            cli.cfhelper,
            ["--config", os.path.join(CONFIG_DIR, "not_valid_yaml.cfh"), "deploy"],
            catch_exceptions=False,
        )


@mock.patch.object(deploy, "deploy_or_update")
def test_valid_multistacks_config(mock_deploy):
    """Pass a file that contains multiple valid stacks"""
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
    mock_deploy.assert_called_once_with("MyStackName", mock.ANY, mock.ANY, mock.ANY)


@mock.patch.object(deploy, "deploy_or_update")
def test_valid_singlestack_config(mock_deploy):
    """Pass a file that contains a single valid stacks"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_singlestack.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
    )
    mock_deploy.assert_called_once_with("MyStackName", mock.ANY, False, set())


@mock.patch.object(deploy, "deploy_or_update")
def test_bad_capability(mock_deploy):
    """Pass a file that contains an invalid capability"""
    runner = CliRunner()

    with pytest.raises(Exception):
        runner.invoke(
            cli.cfhelper,
            [
                "--config",
                os.path.join(CONFIG_DIR, "valid_singlestack_bad_capability.cfh"),
                "deploy",
                "MyStackAlias",
            ],
            catch_exceptions=False,
        )

    mock_deploy.assert_not_called()


@mock.patch.object(deploy, "deploy_or_update")
def test_with_capability(mock_deploy):
    """Pass a file that contains one valid capability"""
    runner = CliRunner()

    runner.invoke(
        cli.cfhelper,
        [
            "--config",
            os.path.join(CONFIG_DIR, "valid_singlestack_with_capability.cfh"),
            "deploy",
            "MyStackAlias",
        ],
        catch_exceptions=False,
    )
    mock_deploy.assert_called_once_with(
        "MyStackName", mock.ANY, False, {"CAPABILITY_IAM"}
    )


@mock.patch.object(deploy, "deploy_or_update")
def test_with_multiple_capabilities(mock_deploy):
    """Pass a file that contains multiple valid capabilities"""
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
    mock_deploy.assert_called_once_with(
        "MyStackName", mock.ANY, False, {"CAPABILITY_IAM", "CAPABILITY_NAMED_IAM"}
    )
