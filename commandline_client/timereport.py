import click

from use_cases.activity_report import format_seconds_returnbed_by_report, TimeSpentInCategoryReport


ACTIVITY_DEFAULT_ARGUMENT = 'all_activities'


def validate_positive_int(ctx, param, value):
    if value < 0:
        raise click.BadParameter('Value must be zero or positive')
    return value


@click.command()
@click.option(
    '--days',
    help='Generate report on how you spent your time during the last x days, 0 = today, 1 = today and yesterday',
    default=0,
    type=int,
    callback=validate_positive_int
)
@click.option(
    '--activity',
    help='Specify the type of category you want to see the report on.',
    default=ACTIVITY_DEFAULT_ARGUMENT
)
def cli(days, activity):
    """
    See a report on how you've spent your time on specific activities or all activity.
    You can see this report for today or the last X days, x being an integer.
    For example,
    To see how much time you've spent working today, type "timereport --activity working"
    To see how much time you've spent working the last 3 days, type "timereport --activity working --days=3"
    To see how you spent your time today, type "timereport"
    To see how you spent your time during the last 3 days type "timereport --days 3"
    """
    if activity != ACTIVITY_DEFAULT_ARGUMENT:
        if not days:
            days_text = 'today'
        elif days == 1:
            days_text = 'since yesterday'
        else:
            days_text = 'during the last {} days'.format(days)
        click.echo(
            "So far, you've spent {} on {} {}!".format(
                format_seconds_returnbed_by_report(
                    TimeSpentInCategoryReport.generate_for_this_category_of_activity(activity, days)[activity]
                ),
                activity,
                days_text
            )
        )
    else:
        click.echo('{} {}'.format(days, activity))
