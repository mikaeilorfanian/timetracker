from ...gateway.activity_gateway import ActivitySearch, ActivityPersistor


def test_correct_user_activities_are_found_when_user_has_multiple_activities(
        test_user, test_sleeping_activity, test_working_activity, test_db):

    test_db['activities'][test_user._id] = [test_sleeping_activity,
                                            test_working_activity]
    activities = ActivitySearch.user_activities(test_user)

    assert len(activities) == 2


def test_no_user_activities_are_found_when_user_has_no_activities(test_user):
    activities = ActivitySearch.user_activities(test_user)
    assert len(activities) == 0


def test_new_activity_added_to_db(test_db, test_user, test_activity):
    assert len(ActivitySearch.user_activities(test_user)) == 1
