import click


@click.command()
@click.argument('activity', default='-', required=True)
def cli(activity):
    """
    Track how much time you spend on different activities throughout the day!
    ACTIVITY is the type of activity you want to start tracking. Examples: working, reading, studying.
    """
    click.echo('Started tracking time for %s' % activity)
