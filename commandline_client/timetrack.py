import click

from use_cases.activity_manager import ActivityManager
from use_cases.activity_report import format_seconds_returnbed_by_report, TimeSpentInCategoryReport


@click.command()
@click.argument('activity', required=True)
def cli(activity):
    """
    Track how much time you spend on different activities throughout the day!
    ACTIVITY is the type of activity you want to start tracking. Examples: working, reading, studying.
    To see a report, use the "timereport" command.
    """

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
