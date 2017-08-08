import arrow
from typing import List

from . import db
from entities.activity import Activity


class RecordNotFoundError(Exception):
    pass


class ActivityGateway:

    @classmethod
    def fetch_from_db(cls, activity: Activity) -> Activity:
        for a in cls.activities():
            if a._id == activity._id:
                return a

        raise RecordNotFoundError('No activity with id %s found in db!' % activity._id)

    @classmethod
    def activities(cls) -> List[Activity]:
        return db.data

    @classmethod
    def activities_today(cls) -> List[Activity]:
        return [activity for activity in cls.activities() if activity.started_on_this_day(arrow.utcnow())]

    @classmethod
    def activities_today_in_this_category(cls, category: str) -> List[Activity]:
        return [activity for activity in cls.activities_today() if activity.category == category]

    @classmethod
    def add_new_activity_to_db(cls, activity: Activity) -> None:
        db.data = db.data.append(activity)
