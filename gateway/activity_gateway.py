import arrow
from typing import List

from . import db
from ..entities.activity import Activity
from ..entities.user import UserEntity


class RecordNotFoundError(Exception):
    pass


class ActivitySearch:

    @classmethod
    def get_activity(cls, user: UserEntity, activity: Activity) -> Activity:
        for a in cls.user_activities(user):
            if a._id == activity._id:
                return a

        raise RecordNotFoundError('No activity with id %s found in db!' % activity._id)

    @classmethod
    def user_activities(cls, user: UserEntity) -> List[Activity]:
        return db['activities'].get(user._id, [])

    @classmethod
    def user_activities_today(cls, user: UserEntity) -> List[Activity]:
        return [activity for activity in cls.user_activities(user) if activity.started_on_this_day(arrow.utcnow())]

    @classmethod
    def user_activities_today_in_this_category(cls, user: UserEntity, category: str) -> List[Activity]:
        return [activity for activity in cls.user_activities_today(user) if activity.category == category]


class ActivityPersistor:

    @classmethod
    def add_new_activity_to_db(cls, activity: Activity) -> None:
        db['activities'][activity.user._id].append(activity)
