import pytest

from gateway import db
from gateway.activity_gateway import ActivityGateway
from use_cases.activity_manager import ActivityManager


@pytest.fixture(scope='function')
def test_db():
    yield db
    db.delete_db()


@pytest.fixture
def test_sleeping_activity():
    return ActivityManager.start_new_activity('sleeping')


@pytest.fixture
def test_working_activity():
    return ActivityManager.start_new_activity('working')


@pytest.fixture
def test_activity():
    a = ActivityManager.start_new_activity('test_activity')
    ActivityGateway.add_new_activity_to_db(a)
    return a


@pytest.fixture
def test_user_with_multiple_activities_on_multiple_days(test_activity):
    test_activity.end()
    ActivityGateway.update_activity_in_db(test_activity)

    test_sleeping_activity = ActivityManager.start_new_activity('sleeping')
    test_sleeping_activity.started_at = test_sleeping_activity.started_at.shift(days=-1)
    test_sleeping_activity.end()
    ActivityGateway.add_new_activity_to_db(test_sleeping_activity)

    test_working_activity = ActivityManager.start_new_activity('working')
    test_working_activity.started_at = test_working_activity.started_at.shift(days=-2)
    test_working_activity.end()
    ActivityGateway.add_new_activity_to_db(test_working_activity)


@pytest.fixture
def test_user_with_multiple_activities_of_same_category_done_today(test_activity):
    test_activity.end()
    test_activity.ended_at = test_activity.started_at.shift(seconds=2000)
    ActivityGateway.update_activity_in_db(test_activity)

    second_activity = ActivityManager.start_new_activity(test_activity.category)
    second_activity.end()
    second_activity.ended_at = second_activity.started_at.shift(seconds=3000)
    ActivityGateway.add_new_activity_to_db(second_activity)

    third_activity = ActivityManager.start_new_activity(test_activity.category)
    third_activity.end()
    third_activity.ended_at = third_activity.started_at.shift(seconds=3000)
    ActivityGateway.add_new_activity_to_db(third_activity)
