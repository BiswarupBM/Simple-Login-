import pytest

from simplelogincmd.cli.main import cli
from tests.integration.util import list_all_commands


all_commands = list_all_commands(cli)


@pytest.mark.parametrize("command", all_commands)
def test_command_shows_help(command, runner):
    result = runner.invoke(command, ["--help"])
    assert result.exit_code == 0
