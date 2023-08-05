from click.testing import CliRunner

from rio.commands.cmd_list import cli
from rio.commands import cmd_deploy, cmd_undeploy
from rio.utilities import errors


def test_list_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, errors.NoLocalFlagError)
    assert "contact@chainopt.com" in result.output


def test_list_deployed():
    """
    Tests when a package is deployed to ensure that it's name is in the output
    """
    runner = CliRunner()
    runner.invoke(cmd_deploy.cli, ["-l", r"samples/myProject"], input="n\n")
    result = runner.invoke(cli, "-l")
    assert not result.exception
    assert "myProject" in result.output


def test_list_no_deployed():
    """
    Tests when there are no deployed packages and ensures that it says nothing
    """
    runner = CliRunner()
    runner.invoke(cmd_undeploy.cli, ["-l", "--all"], input="y\n")
    result = runner.invoke(cli, "-l")
    assert not result.exception
    assert "No packages deployed." in result.output
