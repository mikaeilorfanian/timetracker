from ...entities.activity import Activity


def test_start_an_activity():
    a = Activity('working')
    a.start()
    assert a.started is True


def test_end_an_activity():
    a = Activity('working')
    a.start()
    a.end()
    assert a.ended is True


def test_activity_has_category():
    a = Activity(category='working')
    assert a.category == 'working'
