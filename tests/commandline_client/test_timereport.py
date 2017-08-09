from click.testing import CliRunner
from typing import List

from commandline_client.timereport import cli
from gateway.activity_gateway import ActivityGateway


def test_when_no_arguments_are_given_a_report_for_all_activities_today_is_displayed():
    pass


class TestReportForOneActivityToday:

    def test_one_day_report_shown_when_days_argument_is_not_given_and_activity_is_specified(self, test_activity):
        test_activity.end()
        test_activity.ended_at = test_activity.started_at.shift(seconds=120)
        ActivityGateway.update_activity_in_db(test_activity)

        runner = CliRunner()
        result = runner.invoke(cli, ['--activity', 'test_activity'])

        assert result.exit_code == 0
        assert result.output.count('\n') == 1
        _assert_in_output(result.output, ['test_activity', 'today', '2 minutes'])

    def test_one_day_report_is_shown_when_days_argument_is_given_as_one_and_activity_is_specified(self, test_activity):
        test_activity.end()
        test_activity.ended_at = test_activity.started_at.shift(seconds=120)
        ActivityGateway.update_activity_in_db(test_activity)

        runner = CliRunner()
        result = runner.invoke(cli, ['--activity', 'test_activity', '--days', '1'])

        assert result.exit_code == 0
        assert result.output.count('\n') == 1
        _assert_in_output(result.output, ['test_activity', 'today', '2 minutes'])


def _assert_in_output(output, tests: List[str]) -> None:
    for test_str in tests:
        assert test_str in output
