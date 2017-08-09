import click


@click.command()
@click.option('--days', help='Generate report on how you spent your time during the last x days, '
                                        '1 means today, 2 means today and yesterday', default=1, type=int)
@click.option('--activity', help='Specify the type of category you want to see the report on.',
              default='all')
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
    click.echo('{} {}'.format(days, activity))
