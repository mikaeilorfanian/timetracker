from ...entities.activity import Activity
from ...entities.user import UserEntity


def test_start_an_activity():
    user = UserEntity('mike', _id=1)
    a = Activity(user, 'working')
    a.start()
    assert a.started is True


def test_end_an_activity():
    user = UserEntity('mike', _id=1)
    a = Activity(user, 'working')
    a.start()
    a.end()
    assert a.ended is True


def test_activity_has_category():
    user = UserEntity('mike', _id=1)
    a = Activity(user, category='working')
    assert a.category == 'working'
