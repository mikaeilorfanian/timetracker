from entities.activity import Activity
from gateway.activity_gateway import ActivityGateway


class AnotherActivityInProgressError(Exception):
    pass


class ActivityManager:

    @classmethod
    def start_tracking_new_activity(cls, category: str) -> Activity:
        cls.stop_tracking_last_activity()
        a = cls.start_new_activity(category)
        ActivityGateway.add_new_activity_to_db(a)
        return a

    @classmethod
    def stop_tracking_last_activity(cls) -> None:
        try:
            a = ActivityGateway.fetch_last_activity_started()
            a.end()
            ActivityGateway.update_activity_in_db(a)
        except IndexError:
            pass

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
