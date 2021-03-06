from collections import defaultdict
from typing import Dict

from gateway.activity_gateway import ActivityGateway


class TimeSpentInCategoryReport:

    @classmethod
    def generate_for_this_category_of_activity(cls, category: str, days: int) -> Dict[str, int]:
        total_activity_length = 0

        if days == 0:
            for activity in ActivityGateway.activities_today_in_this_category(category):
                total_activity_length += activity.length
        else:
            for activity in ActivityGateway.activities_in_last_n_days_in_this_category(days, category):
                total_activity_length += activity.length

        return {category: total_activity_length}

    @classmethod
    def generate_for_all_categories_of_activity(cls, days: int) -> Dict[str, int]:
        activities_length = defaultdict(int)

        for activity in ActivityGateway.activities_in_the_last_n_days(days):
            activities_length[activity.category] += activity.length

        return activities_length


def format_seconds_returnbed_by_report(seconds):
    if seconds > 0 and seconds < 60:
        return _seconds_to_seconds(seconds)
    elif seconds >= 60 and seconds < 3600:
        return _seconds_to_minutes(seconds)
    elif seconds == 0:
        return 'exactly zero'
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


class MultipleActivitiesReportDisplayer:

    def __init__(self, report: Dict[str, int]):
        self.report = report
        self.report_text = ''

    def display(self):
        if not self.report:
            return self._report_is_empty_error()

        self._add_header()
        self._enter()

        for activity in self.report:
            self._add_activity_summary(activity, self.report[activity])
            self._enter()

        return self.report_text

    def _add_header(self):
        self.report_text += 'Activity\tTime Spent'

    def _add_activity_summary(self, activity_category: str, activity_length: int):
        self.report_text += '{} \t{}'.format(activity_category, format_seconds_returnbed_by_report(activity_length))

    def _enter(self):
        self.report_text += '\n'

    def _report_is_empty_error(self):
        return 'There are no activities to report on!'
