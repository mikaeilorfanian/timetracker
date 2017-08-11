import click

from gateway.activity_gateway import ActivityGateway
from use_cases.activity_manager import ActivityManager
from use_cases.activity_report import format_seconds_returnbed_by_report, TimeSpentInCategoryReport


RESERVED_ARGUMENTS = [
    'stop',
]


STOP_TRACKING_TIME_ARGUMENT = 'stop'


@click.command()
@click.argument('activity', required=True)
def cli(activity):
    """
    Track how much time you spend on different activities throughout the day!
    ACTIVITY is the type of activity you want to start tracking. Examples: working, reading, studying.
    To see a report, use the "timereport" command.
    """

    if activity in RESERVED_ARGUMENTS:
        if activity.lower() == STOP_TRACKING_TIME_ARGUMENT:
            try:
                last_activity = ActivityGateway.fetch_last_activity_started()
                ActivityManager.stop_tracking_last_activity()
                click.echo('Stopped tracking {}'.format(last_activity.category))
            except IndexError:
                click.echo('I was not tracking any activity!')

    else:
        a = ActivityManager.start_tracking_new_activity(activity)
        click.echo('Started tracking "%s".' % a.category)
        click.echo(
            "So far, you've spent {} on {} today!".format(
                format_seconds_returnbed_by_report(
                    TimeSpentInCategoryReport.generate_for_this_category_of_activity(activity, 0)[activity]
                ),
                activity
            )
        )
