from typing import List

from . import db
from ..entities.activity import Activity
from ..entities.user import UserEntity


class ActivitySearch:

    @classmethod
    def in_progress_activities_for_user(cls, user: UserEntity) -> List[Activity]:
        return db['activities'].get(user._id, [])


class ActivityPersistor:

    @classmethod
    def persist_new_activity(cls, activity: Activity) -> None:
        user_activities= db['activities'].get(activity.user._id, [])
        user_activities.append(activity)
