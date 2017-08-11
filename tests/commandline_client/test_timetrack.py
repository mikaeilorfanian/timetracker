from click.testing import CliRunner

from commandline_client.timetrack import cli
from gateway.activity_gateway import ActivityGateway
from test_timereport import _assert_in_output


class TestTrackActivityCommand:

    def test_track_new_activity_for_the_first_time(self):
        assert len(ActivityGateway.activities()) == 0

        runner = CliRunner()
        result = runner.invoke(cli, ['working'])

        assert result.exit_code == 0
        assert result.output.count('\n') == 2
        _assert_in_output(result.output, ['Started', 'tracking', 'working', 'So far', 'spent', 'today'])

    def test_track_new_activity_when_another_one_is_already_being_tracked(self, test_activity):
        assert len(ActivityGateway.activities()) == 1
        assert test_activity.ended is False

        runner = CliRunner()
        result = runner.invoke(cli, ['working'])

        assert result.exit_code == 0
        assert result.output.count('\n') == 2
        _assert_in_output(result.output, ['Started', 'tracking', 'working', 'So far', 'spent', 'today'])

        assert ActivityGateway.fetch_activity(test_activity).ended is True
        assert len(ActivityGateway.activities()) == 2

    def test_new_ativity_to_track_is_same_category_of_the_last_activity_being_tracked(self, test_activity):
        assert len(ActivityGateway.activities()) == 1
        assert test_activity.ended is False

        runner = CliRunner()
        result = runner.invoke(cli, [test_activity.category])

        assert result.exit_code == 0
        assert result.output.count('\n') == 2
        _assert_in_output(result.output, ['Started', 'tracking', test_activity.category, 'So far', 'spent', 'today'])

        assert ActivityGateway.fetch_activity(test_activity).ended is True
        assert len(ActivityGateway.activities()) == 2


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
