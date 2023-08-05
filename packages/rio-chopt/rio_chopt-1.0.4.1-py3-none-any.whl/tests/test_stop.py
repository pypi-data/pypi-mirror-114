from click.testing import CliRunner

from rio.commands.cmd_stop import cli
from rio.commands import cmd_deploy, cmd_start
from rio.utilities.errors import *


def test_stop_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, NoLocalFlagError)


def test_stop_base():
    """
    Tests the stopping of a deployed package
    """
    runner = CliRunner()
    res1 = runner.invoke(cmd_deploy.cli, ['-l', r'samples/myProject'], input="y\n\n")
    assert not res1.exception
    assert res1.output
    result = runner.invoke(cli, ["-l", "-p", "myProject"])
    assert not result.exception
    assert "package has been stopped" in result.output


def test_stop_missing_input():
    """
    Tests running command with no input
    """
    runner = CliRunner()
    res1 = runner.invoke(cmd_deploy.cli, ['-l', r'samples/myProject'], input="y\n\n")
    assert not res1.exception
    assert res1.output
    result = runner.invoke(cli, ["-l"])
    assert isinstance(result.exception, MissingPackageInputError)
    assert "Please specify a package name or --all." in result.output