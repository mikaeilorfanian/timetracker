from entities.activity import Activity
from gateway.activity_gateway import ActivityGateway


class ActivityWithSameCategoryExistsError(Exception):
    pass


class ActivityManager:

    @classmethod
    def start_new_activity(cls, category):
        if cls.user_already_started_an_activity():
            raise ActivityWithSameCategoryExistsError
        elif cls.user_already_started_activity_of_same_category(category):
            raise ActivityWithSameCategoryExistsError
        else:
            a = Activity(category)
            a.start()
            return a

    @classmethod
    def user_already_started_activity_of_same_category(cls, category):
        user_activities = ActivityGateway.user_activities()
        for activity in user_activities:
            if activity.category == category and activity.started:
                return True
        return False

    @classmethod
    def user_already_started_an_activity(cls):
        user_activities = ActivityGateway.user_activities()
        for activity in user_activities:
            if activity.started:
                return True
        return False

    @classmethod
    def end_activity(cls, activity):
        a = ActivityGateway.fetch_from_db(activity)
        a.end()
