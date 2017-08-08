from typing import Dict

from gateway.activity_gateway import ActivityGateway


class TimeSpentInCategoryReport:

    @classmethod
    def generate_for_this_category_of_activity(cls, category: str) -> Dict[str, int]:
        total_activity_length = 0
        for activity in ActivityGateway.activities_today_in_this_category(category):
            total_activity_length += activity.length

        return {category: total_activity_length}
