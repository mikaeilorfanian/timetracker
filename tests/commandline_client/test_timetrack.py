from click.testing import CliRunner

from commandline_client.timetrack import cli
from gateway.activity_gateway import ActivityGateway
from test_timereport import _assert_in_output


class TestStopTrackingTimeComamnd:

    def test_last_activity_ends_no_new_activity_is_created(self, test_activity):
        assert len(ActivityGateway.activities()) == 1
        assert test_activity.ended is False

        runner = CliRunner()
        result = runner.invoke(cli, ['stop'])

        assert result.exit_code == 0
        assert result.output.count('\n') == 1
        _assert_in_output(result.output, ['Stopped', test_activity.category])

        assert ActivityGateway.fetch_last_activity_started().ended is True
        assert len(ActivityGateway.activities()) == 1

    def test_theres_no_activity_being_tracked_when_stop_command_is_issued(self):
        assert len(ActivityGateway.activities()) == 0

        runner = CliRunner()
        result = runner.invoke(cli, ['stop'])

        assert result.exit_code == 0
        assert result.output.count('\n') == 1
        _assert_in_output(result.output, ['not tracking'])
