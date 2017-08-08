import pytest

from use_cases.activity_manager import (
    ActivityManager,
    ActivityWithSameCategoryExistsError,
    AnotherActivityInProgressError,
)

from gateway.activity_gateway import ActivityGateway
from entities.activity import Activity
from gateway import db


def test_user_cant_start_more_than_one_activity_in_same_category_at_once():
    a = Activity('working')
    a.start()
    db.data = [a]

    with pytest.raises(ActivityWithSameCategoryExistsError):
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
        ActivityManager.end_activity(test_activity)
        assert test_activity.ended_at is not None
        assert test_activity.status != test_activity.STARTED
        assert ActivityGateway.fetch_from_db(test_activity).status == test_activity.ENDED
