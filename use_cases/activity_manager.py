from entities.activity import Activity
from gateway.activity_gateway import ActivityGateway


class AnotherActivityInProgressError(Exception):
    pass


class ActivityManager:

    @classmethod
    @classmethod
    def stop_tracking_last_activity(cls) -> None:
        a = ActivityGateway.fetch_last_activity_started()
        a.end()
        ActivityGateway.update_activity_in_db(a)

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
