from click.testing import CliRunner
from pyboot.cli import main as cli


class TestCli(object):

    def test_project_creation(self, tmpdir):
        """Check if the project is created from the right template."""
        runner = CliRunner()
        # create a new project in tmpdir
        runner.invoke(cli, ['cli', '-d', str(tmpdir), 'myproject'])
        # check everything is there
        assert len(tmpdir.listdir()) == 6
