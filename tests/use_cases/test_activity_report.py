import pytest
from typing import List

from gateway.activity_gateway import ActivityGateway
from tests.utils import make_activity
from use_cases.activity_manager import ActivityManager
from use_cases.activity_report import format_seconds_returnbed_by_report
from use_cases.activity_report import TimeSpentInCategoryReport


class TestTodayReportForSpecificActivity:

    def test_report_shows_length_zero_when_activity_was_not_performed_today(self, test_db):
        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity('working_hard', 0)
        assert report['working_hard'] == 0


    def test_total_activity_length_is_correct_activity_was_performed_once_today_and_already_ended(self,
                                                                                                  test_db,
                                                                                                  test_activity):
        test_activity.end()
        test_activity.ended_at = test_activity.started_at.shift(seconds=100)
        ActivityGateway.update_activity_in_db(test_activity)

        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_activity.category, 0)
        assert report[test_activity.category] == 100

    def test_total_activity_length_is_correct_activity_was_performed_once_today_and_hasnt_ended(self,
                                                                                                  test_db,
                                                                                                  test_activity):
        test_activity.started_at = test_activity.started_at.shift(seconds=-1000)
        ActivityGateway.update_activity_in_db(test_activity)
        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_activity.category, 0)
        assert report[test_activity.category] == 1000

    def test_activity_was_performed_multiple_times_today_and_they_all_already_ended(
            self, test_db, test_user_with_multiple_activities_of_same_category_done_today, test_activity):
        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_activity.category, 0)
        assert report[test_activity.category] == 8000

    def test_activity_was_performed_multiple_times_today_and_all_except_one_already_ended(
            self, test_db, test_user_with_multiple_activities_of_same_category_done_today, test_activity):
        unfinished_activity = ActivityManager.start_new_activity(test_activity.category)
        unfinished_activity.started_at = unfinished_activity.started_at.shift(seconds=-500)
        ActivityGateway.add_new_activity_to_db(unfinished_activity)

        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_activity.category, 0)
        assert report[test_activity.category] == 8500


    def test_activity_performed_multiple_times_on_different_days(self, test_activity):
        test_activity.started_at = test_activity.started_at.shift(seconds=-2000)
        test_activity.end()
        ActivityGateway.update_activity_in_db(test_activity)

        make_activity(1, 3000, test_activity.category)
        make_activity(2, 1000, test_activity.category)
        make_activity(3, 500, test_activity.category)

        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_activity.category, 2)
        assert report[test_activity.category] == 6000


class TestUtilityFunctionThatPrettyPrintsSecondsFromTheReports:

    def test_throws_error_when_it_gets_wrong_values_like_negative_numbers_and_non_integers(self):
        with pytest.raises(ValueError):
            print(format_seconds_returnbed_by_report(-1))
        with pytest.raises(TypeError):
            format_seconds_returnbed_by_report('23')

    def test_shows_seconds_when_number_of_seconds_doesnt_reach_minutes(self):
        assert 'seconds' in format_seconds_returnbed_by_report(59)
        assert '59' in format_seconds_returnbed_by_report(59)

        assert 'second' in format_seconds_returnbed_by_report(1) and not 'seconds' in \
                                                                         format_seconds_returnbed_by_report(1)
        assert '1' in format_seconds_returnbed_by_report(1)

        assert 'seconds' in format_seconds_returnbed_by_report(22)
        assert '22' in format_seconds_returnbed_by_report(22)

    def test_shows_minutes_when_number_of_seconds_doesnt_reach_hours_but_reaches_minutes(self):
        assert 'minute' in format_seconds_returnbed_by_report(60) and not 'minutes' in \
                                                                          format_seconds_returnbed_by_report(60)
        assert '1' in format_seconds_returnbed_by_report(60)

        assert 'minute' in format_seconds_returnbed_by_report(61) and not 'minutes' in \
                                                                          format_seconds_returnbed_by_report(60)
        assert '1' in format_seconds_returnbed_by_report(61)

        assert 'minute' in format_seconds_returnbed_by_report(119) and not 'minutes' in \
                                                                          format_seconds_returnbed_by_report(60)
        assert '1' in format_seconds_returnbed_by_report(119)

        assert 'minutes' in format_seconds_returnbed_by_report(120)
        assert '2' in format_seconds_returnbed_by_report(120)

        assert 'minutes' in format_seconds_returnbed_by_report(2345)
        assert '39' in format_seconds_returnbed_by_report(2345)

        assert 'minutes' in format_seconds_returnbed_by_report(3599)
        assert '59' in format_seconds_returnbed_by_report(3599)

    def test_shows_hours_and_minutes_and_no_seconds_when_number_of_seconds_reaches_hours(self):
        # no minutes when the number of minutes is zero
        self._assert_these_strings_are_in_the_result(3600, ['hour', '1'])
        self._assert_these_strings_are_not_in_the_result(3600, ['hours', 'minutes', 'minute', 'seconds', 'second'])

        self._assert_these_strings_are_in_the_result(6199, ['hour', 'minutes', '43'])
        self._assert_these_strings_are_not_in_the_result(6199, ['hours', 'seconds', 'second'])

        self._assert_these_strings_are_not_in_the_result(7200, ['seconds', 'second', 'minutes', 'minute'])
        self._assert_these_strings_are_in_the_result(7200, ['hours', '2'])

        self._assert_these_strings_are_not_in_the_result(10000, ['seconds', 'second'])
        self._assert_these_strings_are_in_the_result(10000, ['hours', '2', 'minutes', '46'])

        self._assert_these_strings_are_not_in_the_result(10800, ['seconds', 'second', 'minute', 'minutes'])
        self._assert_these_strings_are_in_the_result(10800, ['hours', '3'])

        # no seconds and no minutes when the number of seconds doesn't reach 60
        self._assert_these_strings_are_not_in_the_result(10801, ['seconds', 'second', 'minute', 'minutes'])
        self._assert_these_strings_are_in_the_result(10801, ['hours', '3'])

        # no seconds and no minutes when the number of seconds doesn't reach 60
        self._assert_these_strings_are_not_in_the_result(3601, ['seconds', 'second', 'minute', 'minutes'])
        self._assert_these_strings_are_in_the_result(3601, ['hour', '1'])

        # no seconds and no minutes when the number of seconds doesn't reach 60
        self._assert_these_strings_are_not_in_the_result(3610, ['seconds', 'second', 'minute', 'minutes'])
        self._assert_these_strings_are_in_the_result(3610, ['hour', '1'])

        self._assert_these_strings_are_not_in_the_result(4987, ['seconds', 'second'])
        self._assert_these_strings_are_in_the_result(4987, ['hour', '1', '23', 'minutes'])

        # singular unit for minutes --> "minute"
        self._assert_these_strings_are_in_the_result(7261, ['hours', '2', '1', 'minute'])
        self._assert_these_strings_are_not_in_the_result(7261, ['seconds', 'second'])

        self._assert_these_strings_are_in_the_result(7315, ['hours', '2', '1', 'minute'])
        self._assert_these_strings_are_not_in_the_result(7315, ['seconds', 'second'])

        self._assert_these_strings_are_in_the_result(7592, ['hours', '2', '6', 'minutes'])
        self._assert_these_strings_are_not_in_the_result(7592, ['seconds', 'second'])


    def test_prints_nothing_when_it_receives_zero_seconds(self):
        assert 'nothing' in format_seconds_returnbed_by_report(0)

    def _assert_these_strings_are_in_the_result(self, seconds: int, strings_list: List[str]) -> None:
        for string in strings_list:
            assert string in format_seconds_returnbed_by_report(seconds)

    def _assert_these_strings_are_not_in_the_result(self, seconds: int, strings_list: List[str]) -> None:
        for string in strings_list:
            assert string not in format_seconds_returnbed_by_report(seconds)
