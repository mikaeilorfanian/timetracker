from gateway.activity_gateway import ActivityGateway
from use_cases.activity_manager import ActivityManager


def make_activity(started_days_ago, length_in_seconds, category):
    if started_days_ago == 0:
        seconds_to_shift = length_in_seconds
    else:
        seconds_to_shift = 0

    act1 = ActivityManager.start_tracking_new_activity(category)
    act1.started_at = act1.started_at.shift(days=-started_days_ago, seconds=-seconds_to_shift)
    act1.end()
    act1.ended_at = act1.started_at.shift(seconds=length_in_seconds)
    ActivityGateway.update_activity_in_db(act1)
