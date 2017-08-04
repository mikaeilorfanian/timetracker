import arrow
from arrow import Arrow


class Activity:
    STARTED = 'started'
    ENDED = 'ended'

    def __init__(self, user, category):
        self.status = None
        self.category = category
        self.user = user
        self.started_at = None
        self.ended_at = None

    def start(self):
        self.status = self.STARTED
        self.started_at = arrow.utcnow()

    def end(self):
        self.status = self.ENDED
        self.ended_at = arrow.utcnow()

    @property
    def started(self):
        return self.status == self.STARTED

    @property
    def ended(self):
        return self.status == self.ENDED

    def started_on_this_day(self, date: Arrow) -> bool:
        return all((
            self.started_at.year == date.year,
            self.started_at.month == date.month,
            self.started_at.day == date.day
        ))

    @property
    def length(self) -> int:
        if self.ended_at < self.started_at:
            return 0

        return (self.ended_at - self.started_at).seconds
