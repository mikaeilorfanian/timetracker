from click.testing import CliRunner
from typing import List

from commandline_client.timereport import cli
from gateway.activity_gateway import ActivityGateway
from tests.utils import make_activity


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

    def test_one_day_report_is_shown_when_days_argument_is_given_as_zero_and_activity_is_specified(self,
                                                                                                   test_activity):
        test_activity.end()
        test_activity.ended_at = test_activity.started_at.shift(seconds=120)
        ActivityGateway.update_activity_in_db(test_activity)

        runner = CliRunner()
        result = runner.invoke(cli, ['--activity', 'test_activity', '--days', '0'])

        assert result.exit_code == 0
        assert result.output.count('\n') == 1
        _assert_in_output(result.output, ['test_activity', 'today', '2 minutes'])



class TestReportOneActivityMoreThanOneDay:

    def test_two_report_shows_correct_information_about_specified_category_of_activity(self):
        make_activity(0, 1000, 'working')
        make_activity(1, 2000, 'working')
        make_activity(2, 3000, 'working')
        make_activity(0, 100, 'workin')
        make_activity(-1, 200, 'workin')

        runner = CliRunner()
        result = runner.invoke(cli, ['--activity', 'working', '--days', '2'])

        print(ActivityGateway.activities())

        assert result.exit_code == 0
        assert result.output.count('\n') == 1
        _assert_in_output(result.output, ['working', 'last 2 days', '1 hour', '40 minutes'])

        runner = CliRunner()
        result = runner.invoke(cli, ['--activity', 'workin', '--days', '1'])

        assert result.exit_code == 0
        assert result.output.count('\n') == 1
        _assert_in_output(result.output, ['since yesterday', '5 minutes'])


class TestValidatePositiveIntegersFunction:

    def test_error_raised_when_value_is_negative(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--days', '-2'])

        assert result.exit_code == 2
        assert 'Error' in result.output
        assert '--days' in result.output

    def test_no_error_raised_when_value_is_positive(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--days', '2'])

        assert result.exit_code == 0


def _assert_in_output(output, tests: List[str]) -> None:
    for test_str in tests:
        assert test_str in output
