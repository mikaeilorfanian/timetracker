from ...gateway.activity_gateway import ActivitySearch, ActivityPersistor
from ...use_cases.activity_manager import ActivityManager


def test_correct_user_activities_are_found_when_user_has_multiple_activities(
        test_user, test_sleeping_activity, test_working_activity, test_db):

    test_db['activities'][test_user._id] = [test_sleeping_activity,
                                            test_working_activity]
    activities = ActivitySearch.user_activities(test_user)

    assert len(activities) == 2


def test_no_user_activities_are_found_when_user_has_no_activities(test_user):
    activities = ActivitySearch.user_activities(test_user)
    assert len(activities) == 0


def test_new_activity_added_to_db(test_db, test_user, test_activity):
    assert len(ActivitySearch.user_activities(test_user)) == 1


class TestSearchUserActivitiesStartedToday:

    def test_no_activities_returned_when_nothing_started_today(self, test_db, test_user):
        assert len(ActivitySearch.user_activities_today(test_user)) == 0

    def test_one_activity_returned_when_only_one_started_today(self, test_db, test_activity, test_user):
        todays_activities = ActivitySearch.user_activities_today(test_user)
        assert len(todays_activities) == 1
        assert test_activity in todays_activities

    def test_user_has_activities_on_different_days_but_only_1_today(self, test_user_with_multiple_activities_on_multiple_days, test_activity, test_db):
        test_user = test_user_with_multiple_activities_on_multiple_days
        todays_activities = ActivitySearch.user_activities_today(test_user)
        assert len(todays_activities) == 1
        assert test_activity in todays_activities

    def test_user_has_more_than_one_activity_today_and_more_on_other_days(self, test_user_with_multiple_activities_on_multiple_days, test_db, test_activity):
        test_user = test_user_with_multiple_activities_on_multiple_days
        test_working_activity = ActivityManager.start_new_activity(test_user, 'working')
        ActivityPersistor.add_new_activity_to_db(test_working_activity)

        todays_activities = ActivitySearch.user_activities_today(test_user)
        assert len(todays_activities) == 2
        assert test_activity in todays_activities
        assert test_working_activity in todays_activities
