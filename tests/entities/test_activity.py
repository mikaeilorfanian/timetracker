import arrow


def test_start_an_activity(test_activity):
    test_activity.start()
    assert test_activity.started is True
    assert test_activity.started_at is not None
    assert test_activity.ended_at is None
    assert test_activity._id is not None


def test_end_an_activity(test_activity):
    test_activity.start()
    test_activity.end()
    assert test_activity.started_at is not None
    assert test_activity.ended is True
    assert test_activity.ended_at is not None


def test_activity_has_category(test_activity):
    assert test_activity.category is not None


class TestActivityStartedOnSpecificDayMethod:

    def test_activity_started_today_returns_true_for_todays_date(self, test_db, test_activity):
        assert test_activity.started_on_this_day(arrow.utcnow()) is True

    def test_activity_not_started_today_returns_false_for_todays_date(self, test_db, test_activity):
        test_activity.started_at = test_activity.started_at.shift(days=-2)
        assert test_activity.started_on_this_day(arrow.utcnow()) is False

    def test_activit_started_2_days_ago_return_true_when_date_is_for_2_days_ago(self, test_db, test_activity):
        test_activity.started_at = test_activity.started_at.shift(days=-2)
        assert test_activity.started_on_this_day(arrow.utcnow().shift(days=-2)) is True


class TestActivityStartedOnOrAfterThisDayMethod:

    def test_activity_started_on_the_day_returns_true(self, test_activity):
        assert test_activity.started_on_or_later_than_this_day(arrow.utcnow()) is True

    def test_activity_started_before_that_day_returns_false(self, test_activity):
        test_activity.started_at = test_activity.started_at.shift(days=-3)
        prev_date = arrow.utcnow().shift(days=-2)
        assert test_activity.started_on_or_later_than_this_day(prev_date) is False


    def test_activity_started_after_that_day_returns_true(self, test_activity):
        test_activity.started_at = test_activity.started_at.shift(days=-5)
        prev_date = arrow.utcnow().shift(days=-9)
        assert test_activity.started_on_or_later_than_this_day(prev_date) is True

    def test_activity_without_start_date_returns_false(self, test_activity):
        test_activity.started_at = None
        assert test_activity.started_on_or_later_than_this_day(arrow.utcnow()) is False
