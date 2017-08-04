import pytest

from ...use_cases.activity_manager import ActivityManager, \
    ActivityWithSameCategoryExistsError
from ...entities.activity import Activity
from ...entities.user import UserEntity
from ...gateway import db


def test_user_cant_start_more_than_one_activity_in_same_category_at_once():
    user = UserEntity('mike', _id=1)
    a = Activity(user, 'working')
    a.start()
    db['activities'] = dict()
    db['activities'][user._id] = [a]

    with pytest.raises(ActivityWithSameCategoryExistsError):
        ActivityManager.start_new_activity(user, 'working')


def test_user_cant_engage_in_more_than_one_activity_at_once():
    user = UserEntity('mike', _id=1)
    a = Activity(user, 'working')
    a.start()
    db['activities'] = dict()
    db['activities'][user._id] = [a]

    with pytest.raises(ActivityWithSameCategoryExistsError):
        ActivityManager.start_new_activity(user, 'sleeping')


def test_different_users_can_start_same_activity_in_same_category_at_once():
    user1 = UserEntity('mike', _id=1)
    a1 = Activity(user1, 'working')
    a1.start()
    db['activities'] = dict()
    db['activities'][user1._id] = [a1]

    user2 = UserEntity('Garry', _id=2)
    a2 = ActivityManager.start_new_activity(user2, 'working')
    db['activities'][user1._id].append(a2)

def test_different_users_can_engage_in_different_activities_at_once():
    user1 = UserEntity('mike', _id=1)
    a1 = Activity(user1, 'working')
    a1.start()
    db['activities'] = dict()
    db['activities'][user1._id] = [a1]

    user2 = UserEntity('Garry', _id=2)
    a2 = ActivityManager.start_new_activity(user2, 'sleeping')
    db['activities'][user1._id].append(a2)


class TestActivityLengthCalculator:

    def test_activity_ended_after_it_started(self, test_activity):
        test_activity.end()
        test_activity.ended_at = test_activity.started_at.shift(seconds=100)
        assert test_activity.length == 100

    def test_activity_started_after_it_ended(self, test_activity):
        test_activity.end()
        test_activity.ended_at = test_activity.started_at.shift(seconds=-100)
        assert test_activity.length == 0
