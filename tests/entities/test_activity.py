def test_start_an_activity(test_activity):
    test_activity.start()
    assert test_activity.started is True
    assert test_activity.started_at is not None
    assert test_activity.ended_at is None


def test_end_an_activity(test_activity):
    test_activity.start()
    test_activity.end()
    assert test_activity.started_at is not None
    assert test_activity.ended is True
    assert test_activity.ended_at is not None


def test_activity_has_category(test_activity):
    assert test_activity.category is not None
