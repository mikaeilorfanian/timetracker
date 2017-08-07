import arrow
from typing import List

from . import db
from ..entities.activity import Activity


class RecordNotFoundError(Exception):
    pass


class ActivitySearch:

    @classmethod
    def fetch_from_db(cls, activity: Activity) -> Activity:
        for a in cls.user_activities():
            if a._id == activity._id:
                return a

        raise RecordNotFoundError('No activity with id %s found in db!' % activity._id)

    @classmethod
    def user_activities(cls) -> List[Activity]:
        return db['activities']

    @classmethod
    def user_activities_today(cls) -> List[Activity]:
        return [activity for activity in cls.user_activities() if activity.started_on_this_day(arrow.utcnow())]

    @classmethod
    def user_activities_today_in_this_category(cls, category: str) -> List[Activity]:
        return [activity for activity in cls.user_activities_today() if activity.category == category]


class ActivityPersistor:

    @classmethod
    def add_new_activity_to_db(cls, activity: Activity) -> None:
        db['activities'].append(activity)
