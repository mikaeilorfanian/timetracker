from collections import defaultdict
import pytest

from ..entities.user import UserEntity
from ..gateway import db
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
    return ActivityManager.start_new_activity(test_user, 'test_activity')
