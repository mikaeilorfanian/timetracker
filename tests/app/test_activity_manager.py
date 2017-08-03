import pytest

from ...app.activity_manager import ActivityManager, \
    ActivityWithSameCategoryExistsError
from ...entities.activity import Activity
from ...gateway import db


def test_cant_start_more_than_one_activity_in_same_category_at_once():
    a = Activity('working')
    a.start()
    db['activities'] = [a]
    with pytest.raises(ActivityWithSameCategoryExistsError):
        ActivityManager.start_new_activity('working')


def test_cant_engage_in_more_than_one_activity_at_once():
    a = Activity('working')
    a.start()
    db['activities'] = [a]
    with pytest.raises(ActivityWithSameCategoryExistsError):
        ActivityManager.start_new_activity('sleeping')
