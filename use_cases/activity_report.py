from typing import Dict

from gateway.activity_gateway import ActivityGateway


class TimeSpentInCategoryReport:

    @classmethod
    def generate_for_this_category_of_activity(cls, category: str) -> Dict[str, int]:
        total_activity_length = 0
        for activity in ActivityGateway.activities_today_in_this_category(category):
            total_activity_length += activity.length

        return {category: total_activity_length}


def format_seconds_returnbed_by_report(seconds):
    if seconds > 0 and seconds < 60:
        return _seconds_to_seconds(seconds)
    elif seconds >= 60 and seconds < 3600:
        return _seconds_to_minutes(seconds)
    elif seconds == 0:
        return 'nothing'
    elif seconds >= 3600:
        return _seconds_to_hours_and_minutes(seconds)
    else:
        raise ValueError


def _seconds_to_hours_and_minutes(seconds):
    hours = seconds // 3600
    hours_unit = 'hour' if hours == 1 else 'hours'
    return '{} {}'.format(hours, hours_unit) + ' ' + _seconds_to_minutes(seconds % 3600)


def _seconds_to_seconds(seconds):
    unit = 'second' if seconds == 1 else 'seconds'
    return '{} {}'.format(seconds, unit)


def _seconds_to_minutes(seconds):
    minutes = seconds // 60
    if minutes == 0:
        return ''

    unit = 'minute' if minutes == 1 else 'minutes'
    return '{} {}'.format(minutes, unit)
