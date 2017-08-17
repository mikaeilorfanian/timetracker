from tests.commandline_client.test_timereport import _assert_in_output
from use_cases.activity_report import MultipleActivitiesReportDisplayer


class TestAllCategoriesOfActivityReportDisplayer:

    def test_reporter_shows_header(self):
        r = MultipleActivitiesReportDisplayer({'working': 10})
        output = r.display()
        _assert_in_output(output, ['Activity', 'Time Spent'])

    def test_reporter_shows_each_activitys_category_and_length(self):
        r = MultipleActivitiesReportDisplayer({'working': 10})
        output = r.display()
        _assert_in_output(output, ['working', '10'])

    def test_reporter_shows_error_message_when_thers_no_activities_in_report(self):
        r = MultipleActivitiesReportDisplayer({})
        output = r.display()
        _assert_in_output(output, ['no', 'activities'])
