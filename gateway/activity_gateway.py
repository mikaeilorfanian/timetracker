import arrow
from typing import List

from . import db
from ..entities.activity import Activity
from ..entities.user import UserEntity


class ActivitySearch:

    @classmethod
    def user_activities(cls, user: UserEntity) -> List[Activity]:
        return db['activities'].get(user._id, [])


    @classmethod
    def user_activities_today(cls, user: UserEntity) -> List[Activity]:
        return [activity for activity in cls.user_activities(user) if activity.started_on_this_day(arrow.utcnow())]


class ActivityPersistor:

    @classmethod
    def add_new_activity_to_db(cls, activity: Activity) -> None:
        db['activities'][activity.user._id].append(activity)
