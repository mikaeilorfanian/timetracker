import pytest

from gateway.activity_gateway import ActivityGateway, RecordNotFoundError
from tests.utils import make_activity
from use_cases.activity_manager import ActivityManager


class TestSearchUserActivities:

    def test_correct_user_activities_are_found_when_user_has_multiple_activities(
            self, test_sleeping_activity, test_working_activity, test_db):

        test_db.data = [test_sleeping_activity, test_working_activity]
        activities = ActivityGateway.activities()

        assert len(activities) == 2


    def test_no_user_activities_are_found_when_user_has_no_activities(self):
        activities = ActivityGateway.activities()
        assert len(activities) == 0

    def test_new_activity_turns_up_in_search_results(self, test_db, test_activity):
        assert len(ActivityGateway.activities()) == 1
        test_activity.end()
        ActivityGateway.update_activity_in_db(test_activity)

        a = ActivityManager.start_new_activity('test2_activity')
        ActivityGateway.add_new_activity_to_db(a)
        assert len(ActivityGateway.activities()) == 2

    def test_activity_updated_is_persisted(self, test_activity):
        a = ActivityGateway.fetch_activity(test_activity)
        assert a.ended is False

        test_activity.end()
        ActivityGateway.update_activity_in_db(test_activity)

        a = ActivityGateway.fetch_activity(test_activity)
        assert a.ended is True

    def test_activity_is_removed_from_db(self, test_activity):
        assert ActivityGateway.fetch_activity(test_activity) is not None
        ActivityGateway.remove_activity_from_db(test_activity)

        with pytest.raises(RecordNotFoundError):
            ActivityGateway.fetch_activity(test_activity)

    def test_correct_last_activity_returned_based_on_when_activity_was_created(
            self, test_user_with_multiple_activities_on_multiple_days):
        latest_activity = ActivityManager.start_new_activity('break')
        ActivityGateway.add_new_activity_to_db(latest_activity)
        assert ActivityGateway.fetch_last_activity_started()._id == latest_activity._id

    def test_correct_last_activity_returned_when_theres_only_one_activity_in_db(self, test_activity):
        assert ActivityGateway.fetch_last_activity_started()._id == test_activity._id

    def test_error_thrown_for_last_activity_started_when_theres_no_activities_in_db(self):
        with pytest.raises(IndexError):
            ActivityGateway.fetch_last_activity_started()


def test_new_activity_added_to_db(test_db, test_activity):
    assert len(ActivityGateway.activities()) == 1


class TestSearchUserActivitiesStartedToday:

    def test_no_activities_returned_when_nothing_started_today(self, test_db):
        assert len(ActivityGateway.activities_today()) == 0

    def test_one_activity_returned_when_only_one_started_today(self, test_db, test_activity):
        todays_activities = ActivityGateway.activities_today()
        assert len(todays_activities) == 1
        assert test_activity._id == todays_activities[0]._id

    def test_user_has_activities_on_different_days_but_only_1_today(self, test_user_with_multiple_activities_on_multiple_days, test_activity, test_db):
        todays_activities = ActivityGateway.activities_today()
        assert len(todays_activities) == 1
        assert test_activity._id == todays_activities[0]._id

    def test_user_has_more_than_one_activity_today_and_more_on_other_days(self, test_user_with_multiple_activities_on_multiple_days, test_db, test_activity):
        test_working_activity = ActivityManager.start_new_activity('working')
        ActivityGateway.add_new_activity_to_db(test_working_activity)

        todays_activities = ActivityGateway.activities_today()
        assert len(todays_activities) == 2
        _ids = [a._id for a in todays_activities]
        assert test_activity._id in _ids
        assert test_working_activity._id in _ids


class TestSearchForUserActivitiesWithSpecificCategoryStartedToday:

    def test_no_activities_returned_when_nothing_started_today(self, test_db):
        assert len(ActivityGateway.activities_today_in_this_category('working')) == 0

    def test_one_activity_returned_when_only_one_started_today(self, test_db, test_activity):
        todays_activities = ActivityGateway.activities_today_in_this_category(test_activity.category)
        assert len(todays_activities) == 1
        assert test_activity._id == todays_activities[0]._id

    def test_user_has_activities_on_different_days_but_only_1_today(self, test_user_with_multiple_activities_on_multiple_days, test_activity, test_db):
        todays_activities = ActivityGateway.activities_today_in_this_category(test_activity.category)
        assert len(todays_activities) == 1
        assert test_activity._id == todays_activities[0]._id

    def test_user_has_more_than_one_activity_today_but_only_one_is_what_we_want_and_more_activities_on_other_days(self, test_user_with_multiple_activities_on_multiple_days, test_db, test_activity):
        test_working_activity = ActivityManager.start_new_activity('working')
        ActivityGateway.add_new_activity_to_db(test_working_activity)

        todays_activities = ActivityGateway.activities_today_in_this_category('working')
        assert len(todays_activities) == 1
        assert test_working_activity._id == todays_activities[0]._id


class TestSearchForActivity:

    def test_correct_activity_is_found(self, test_activity, test_db):
        activity = ActivityGateway.fetch_activity(test_activity)
        assert activity._id == test_activity._id

    def test_exception_thrown_when_no_activity_found_in_db_with_that_id(self, test_db):
        a = ActivityManager.start_new_activity('test_activity')
        with pytest.raises(RecordNotFoundError):
            ActivityGateway.fetch_activity(a)


class TestSearchForActivitiesWithSpecificCategoryStartedOnOrLaterThanSpecificDay:

    def test_no_activities_returned_when_activitie_with_such_category_dont_exist_at_all(self, test_activity):
        test_activity.started_at = test_activity.started_at.shift(days=-2)
        test_activity.end()
        ActivityGateway.update_activity_in_db(test_activity)
        ActivityManager.start_new_activity('sleeping')
        assert len(ActivityGateway.activities_in_last_n_days_in_this_category(2, 'working')) == 0

    def test_no_activities_returned_when_there_are_no_activitie_on_or_after_specificed_day(self, test_activity):
        test_activity.started_at = test_activity.started_at.shift(days=-4)
        test_activity.end()
        ActivityGateway.update_activity_in_db(test_activity)

        assert len(ActivityGateway.activities_in_last_n_days_in_this_category(3, test_activity.category)) == 0

    def test_one_acitivity_returned_when_theres_only_one_with_such_category(self, test_activity):
        test_activity.started_at = test_activity.started_at.shift(days=-3)
        ActivityGateway.update_activity_in_db(test_activity)

        assert len(ActivityGateway.activities_in_last_n_days_in_this_category(3, test_activity.category)) == 1

    def test_only_one_activity_returned_when_the_rest_the_activities_with_such_category_are_on_previous_days(self):
        act1 = ActivityManager.start_tracking_new_activity('working')
        act1.end()
        act1.started_at = act1.started_at.shift(days=-2)
        ActivityGateway.update_activity_in_db(act1)

        act2 = ActivityManager.start_tracking_new_activity('working')
        act2.end()
        act2.started_at = act2.started_at.shift(days=-4)
        ActivityGateway.update_activity_in_db(act2)

        act3 = ActivityManager.start_tracking_new_activity('working')
        act3.end()
        act3.started_at = act2.started_at.shift(days=-3)
        ActivityGateway.update_activity_in_db(act3)

        assert len(ActivityGateway.activities_in_last_n_days_in_this_category(2, 'working')) == 1

    def test_correct_activities_returned_when_there_are_activities_on_and_after_specified_day(self):
        act1 = ActivityManager.start_tracking_new_activity('working')
        act1.end()
        act1.started_at = act1.started_at.shift(days=-2)
        ActivityGateway.update_activity_in_db(act1)

        act2 = ActivityManager.start_tracking_new_activity('working')
        act2.end()
        act2.started_at = act2.started_at.shift(days=-4)
        ActivityGateway.update_activity_in_db(act2)

        act3 = ActivityManager.start_tracking_new_activity('working')
        act3.end()
        act3.started_at = act3.started_at.shift(days=-3)
        ActivityGateway.update_activity_in_db(act3)

        assert len(ActivityGateway.activities_in_last_n_days_in_this_category(4, 'working')) == 3


    def test_number_of_days_is_zero(self, test_activity):
        act1 = ActivityManager.start_tracking_new_activity('working')
        act1.end()
        act1.started_at = act1.started_at.shift(days=-1)
        ActivityGateway.update_activity_in_db(act1)

        act2 = ActivityManager.start_tracking_new_activity('working')
        act2.end()
        act2.started_at = act2.started_at.shift(days=-3)
        ActivityGateway.update_activity_in_db(act2)

        assert len(ActivityGateway.activities_in_last_n_days_in_this_category(0, test_activity.category)) == 1


class TestSearchForActivitiesStartedOnOrLaterThanSpecificDay:

    def test_no_activities_returned_when_there_are_no_activitie_on_or_after_specificed_day(self):
        assert len(ActivityGateway.activities_in_the_last_n_days(3)) == 0

    def test_one_acitivity_returned_when_theres_only_one_activity_in_the_given_range(self, test_activity):
        test_activity.started_at = test_activity.started_at.shift(days=-3)
        ActivityGateway.update_activity_in_db(test_activity)

        assert len(ActivityGateway.activities_in_the_last_n_days(3)) == 1

    def test_correct_activities_returned_when_there_are_activities_on_and_after_specified_day(self):
        make_activity(2, 10000, 'working')
        make_activity(3, 20000, 'sleeping')
        make_activity(4, 20000, 'eating')

        assert len(ActivityGateway.activities_in_the_last_n_days(4)) == 3


    def test_number_of_days_is_zero(self, test_activity):
        make_activity(1, 10000, 'working')
        make_activity(3, 20000, 'sleeping')

        assert len(ActivityGateway.activities_in_the_last_n_days(0)) == 1
