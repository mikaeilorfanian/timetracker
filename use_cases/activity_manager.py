from ..entities.activity import Activity
from ..gateway.activity_gateway import ActivitySearch


class ActivityWithSameCategoryExistsError(Exception):
    pass


class ActivityManager:

    @classmethod
    def start_new_activity(cls, user, category):
        if cls.user_already_started_an_activity(user):
            raise ActivityWithSameCategoryExistsError
        elif cls.user_already_started_activity_of_same_category(user, category):
            raise ActivityWithSameCategoryExistsError
        else:
            a = Activity(user, category)
            a.start()
            return a

    @classmethod
    def user_already_started_activity_of_same_category(cls, user, category):
        user_activities = ActivitySearch.user_activities(user)
        for activity in user_activities:
            if activity.category == category and activity.started:
                return True
        return False

    @classmethod
    def user_already_started_an_activity(cls, user):
        user_activities = ActivitySearch.user_activities(user)
        for activity in user_activities:
            if activity.started:
                return True
        return False
