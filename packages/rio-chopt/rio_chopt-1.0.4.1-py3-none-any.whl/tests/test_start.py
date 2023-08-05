from click.testing import CliRunner

from rio.commands import cmd_undeploy, cmd_deploy
from rio.commands.cmd_start import cli
from rio.utilities import errors


def test_start_nonlocal():
    """
    Tests that not passing the local flag tells one to contact ChainOpt support.
    """
    runner = CliRunner()
    result = runner.invoke(cli)
    assert isinstance(result.exception, errors.NoLocalFlagError)


def test_start_bad_package():
    """
    Tests when a bad package name is passed as input
    """
    runner = CliRunner()
    # Deploys sample package to ensure something is running
    res1 = runner.invoke(cmd_deploy.cli, ['-l', r'samples/myProject'], input="y\n\n")
    assert not res1.exception
    assert res1.output
    result = runner.invoke(cli, ["-l", "-p", "rio-api"])
    assert isinstance(result.exception, errors.PackageExistenceError)


def test_start_no_running_packages():
    """
    Tests when there are no packages running.
    """
    runner = CliRunner()
    # Undeploys ALL packages
    runner.invoke(cmd_undeploy.cli, ["-l", "--all"], input="y\n")
    result = runner.invoke(cli, ["-l", "-p", "rio-api"])
    assert isinstance(result.exception, errors.NoRunningPackagesError)
