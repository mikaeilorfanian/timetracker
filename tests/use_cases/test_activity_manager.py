import pytest

from use_cases.activity_manager import (
    ActivityManager,
    AnotherActivityInProgressError,
)

from gateway.activity_gateway import ActivityGateway
from entities.activity import Activity
from gateway import db


def test_user_cant_start_more_than_one_activity_in_same_category_at_once():
    a = Activity('working')
    a.start()
    db.data = [a]

    with pytest.raises(AnotherActivityInProgressError):
        ActivityManager.start_new_activity('working')


def test_user_cant_engage_in_more_than_one_activity_at_once():
    a = Activity('working')
    a.start()
    db.data = [a]

    with pytest.raises(AnotherActivityInProgressError):
        ActivityManager.start_new_activity('sleeping')


class TestActivityLengthCalculator:

    def test_activity_ended_after_it_started(self, test_activity):
        test_activity.end()
        test_activity.ended_at = test_activity.started_at.shift(seconds=100)
        assert test_activity.length == 100

    def test_activity_started_after_it_ended(self, test_activity):
        test_activity.end()
        test_activity.ended_at = test_activity.started_at.shift(seconds=-100)
        assert test_activity.length == 0


class TestEndActivity:

    def test_after_activity_ends_its_status_changes_and_end_time_is_recorded(self, test_activity):
        test_activity.end()
        ActivityGateway.update_activity_in_db(test_activity)
        assert test_activity.ended_at is not None
        assert test_activity.status != test_activity.STARTED
        assert ActivityGateway.fetch_activity(test_activity).status == test_activity.ENDED

    def test_method_stops_tracking_last_activity_properly_when_theres_only_one_in_db(self, test_activity):
        ActivityManager.stop_tracking_last_activity()
        assert ActivityGateway.fetch_last_activity_started()._id == test_activity._id
        assert ActivityGateway.fetch_last_activity_started().ended

    def test_method_stops_tracking_last_activity_properly_when_there_are_more_than_one_activities_in_db(
            self, test_activity, test_user_with_multiple_activities_on_multiple_days):
        ActivityManager.stop_tracking_last_activity()
        assert ActivityGateway.fetch_last_activity_started()._id == test_activity._id
        assert ActivityGateway.fetch_last_activity_started().ended


class TestStartTrackingActivity:

    def test_starting_to_track_new_activity_automatically_stops_tracking_the_last_one(self, test_activity):
        assert not test_activity.ended
        ActivityManager.start_tracking_new_activity('break')
        assert ActivityGateway.fetch_activity(test_activity).ended

    def test_starting_to_track_new_activity_puts_the_activity_int_the_db(self, test_activity):
        assert len(ActivityGateway.activities()) == 1
        ActivityManager.start_tracking_new_activity('break')
        assert len(ActivityGateway.activities()) == 2
        assert not ActivityGateway.fetch_last_activity_started().ended

    def test_start_tracking_the_first_activity(self):
        ActivityManager.start_tracking_new_activity('break')
        assert len(ActivityGateway.activities()) == 1
