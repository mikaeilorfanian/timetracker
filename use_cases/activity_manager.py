from entities.activity import Activity
from gateway.activity_gateway import ActivityGateway


class AnotherActivityInProgressError(Exception):
    pass


class ActivityManager:

    @classmethod
    def start_new_activity(cls, category):
        if cls.user_already_started_an_activity():
            raise AnotherActivityInProgressError
        else:
            a = Activity(category)
            a.start()
            return a

    @classmethod
    def user_already_started_an_activity(cls):
        user_activities = ActivityGateway.activities()
        for activity in user_activities:
            if activity.started:
                return True
        return False

    @classmethod
    def end_activity(cls, activity):
        a = ActivityGateway.fetch_activity(activity)
        a.end()
