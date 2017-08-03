from . import db


class ActivitySearch:

    @classmethod
    def in_progress_activities(cls):
        return db['activities']
