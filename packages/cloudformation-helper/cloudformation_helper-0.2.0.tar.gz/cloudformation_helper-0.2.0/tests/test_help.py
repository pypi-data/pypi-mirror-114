#!/usr/bin/env python

"""Tests for `cloudformation_helper` package."""

from click.testing import CliRunner

from cloudformation_helper import cli


def test_get_help():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.cfhelper)
    assert result.exit_code == 0
    assert "Usage: cfhelper [OPTIONS] COMMAND [ARGS]..." in result.output
    help_result = runner.invoke(cli.cfhelper, ["--help"])
    assert help_result.exit_code == 0
    assert "Usage: cfhelper [OPTIONS] COMMAND [ARGS]..." in help_result.output
