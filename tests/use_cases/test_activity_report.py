from ...gateway.activity_gateway import ActivityPersistor
from ...use_cases.activity_manager import ActivityManager
from ...use_cases.activity_report import TimeSpentInCategoryReport


class TestTodayReportForSpecificActivity:

    def test_report_shows_length_zero_when_activity_was_not_performed_today(self, test_db, test_user):
        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_user, 'working_hard')
        assert report['working_hard'] == 0


    def test_total_activity_length_is_correct_activity_was_performed_once_today_and_already_ended(self,
                                                                                                  test_db,
                                                                                                  test_activity,
                                                                                                  test_user):
        test_activity.end()
        test_activity.ended_at = test_activity.started_at.shift(seconds=100)

        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_user, test_activity.category)
        assert report[test_activity.category] == 100

    def test_total_activity_length_is_correct_activity_was_performed_once_today_and_hasnt_ended(self,
                                                                                                  test_db,
                                                                                                  test_activity,
                                                                                                  test_user):
        test_activity.started_at = test_activity.started_at.shift(seconds=-1000)
        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_user, test_activity.category)
        assert report[test_activity.category] == 1000

    def test_activity_was_performed_multiple_times_today_and_they_all_already_ended(
            self, test_db, test_user_with_multiple_activities_of_same_category_done_today, test_activity):
        test_user = test_user_with_multiple_activities_of_same_category_done_today
        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_user, test_activity.category)
        assert report[test_activity.category] == 8000

    def test_activity_was_performed_multiple_times_today_and_all_except_one_already_ended(
            self, test_db, test_user_with_multiple_activities_of_same_category_done_today, test_activity):
        test_user = test_user_with_multiple_activities_of_same_category_done_today

        unfinished_activity = ActivityManager.start_new_activity(test_user, test_activity.category)
        ActivityPersistor.add_new_activity_to_db(unfinished_activity)
        unfinished_activity.started_at = unfinished_activity.started_at.shift(seconds=-500)

        report = TimeSpentInCategoryReport.generate_for_this_category_of_activity(test_user, test_activity.category)
        assert report[test_activity.category] == 8500
