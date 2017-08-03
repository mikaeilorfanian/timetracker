from ..entities.activity import Activity
from ..gateway.activity_gateway import ActivitySearch


class ActivityWithSameCategoryExistsError(Exception):
    pass


class ActivityManager:

    @classmethod
    def start_new_activity(cls, user, category):
        if cls.any_activity_already_started(user):
            raise ActivityWithSameCategoryExistsError
        elif cls.activity_with_same_category_already_started(user, category):
            raise ActivityWithSameCategoryExistsError
        else:
            a = Activity(user, category)
            a.start()
            return a

    @classmethod
    def activity_with_same_category_already_started(cls, user, category):
        in_progress_activities = ActivitySearch.\
            in_progress_activities_for_user(user)
        for activity in in_progress_activities:
            if activity.category == category and activity.started:
                return True
        return False

    @classmethod
    def any_activity_already_started(cls, user):
        in_progress_activities = ActivitySearch.\
            in_progress_activities_for_user(user)
        for activity in in_progress_activities:
            if activity.started:
                return True
        return False
