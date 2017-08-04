from collections import defaultdict
import pytest

from ..entities.user import UserEntity
from ..gateway import db
from ..gateway.activity_gateway import ActivityPersistor
from ..use_cases.activity_manager import ActivityManager


@pytest.fixture(scope='function')
def test_db():
    yield db
    db['activities'] = defaultdict(list)


@pytest.fixture
def test_user():
    return UserEntity('mike', _id=1)


@pytest.fixture
def test_sleeping_activity(test_user):
    return ActivityManager.start_new_activity(test_user, 'sleeping')


@pytest.fixture
def test_working_activity(test_user):
    return ActivityManager.start_new_activity(test_user, 'working')


@pytest.fixture
def test_activity(test_user):
    a = ActivityManager.start_new_activity(test_user, 'test_activity')
    ActivityPersistor.add_new_activity_to_db(a)
    return a


@pytest.fixture
def test_user_with_multiple_activities_on_multiple_days(test_user, test_activity):
    test_activity.end()

    test_sleeping_activity = ActivityManager.start_new_activity(test_user, 'sleeping')
    test_sleeping_activity.started_at = test_sleeping_activity.started_at.shift(days=-1)
    ActivityPersistor.add_new_activity_to_db(test_sleeping_activity)
    test_sleeping_activity.end()

    test_working_activity = ActivityManager.start_new_activity(test_user, 'working')
    test_working_activity.started_at = test_working_activity.started_at.shift(days=-2)
    ActivityPersistor.add_new_activity_to_db(test_working_activity)
    test_working_activity.end()

    return test_user
