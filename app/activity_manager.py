from ..entities.activity import Activity
from ..gateway.activity_gateway import ActivitySearch


class ActivityWithSameCategoryExistsError(Exception):
    pass


class ActivityManager:

    @classmethod
    def start_new_activity(cls, category):
        if cls.activity_with_same_category_already_started(category):
            raise ActivityWithSameCategoryExistsError
        else:
            a = Activity(category)
            a.start()
            return a

    @classmethod
    def activity_with_same_category_already_started(cls, category):
        in_progress_activities = ActivitySearch.in_progress_activities()
        for activity in in_progress_activities:
            if activity.started:
                return True
        return False
