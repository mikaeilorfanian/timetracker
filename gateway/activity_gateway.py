from . import db


class ActivitySearch:

    @classmethod
    def in_progress_activities_for_user(cls, user):
        return db['activities'].get(user._id, [])
