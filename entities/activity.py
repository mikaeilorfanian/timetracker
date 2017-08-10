import arrow
from arrow import Arrow
import uuid


class Activity:
    STARTED = 'started'
    ENDED = 'ended'

    def __init__(self, category):
        self.status = None
        self.category = category
        self.started_at = None
        self.ended_at = None
        self._id = uuid.uuid4()

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
        if not self.started_at:
            return False

        return all((
            self.started_at.year == date.year,
            self.started_at.month == date.month,
            self.started_at.day == date.day
        ))

    def started_on_or_later_than_this_day(self, date: Arrow) -> bool:
        if self.started_on_this_day(date):
            return True
        elif not self.started_at:
            return False
        else:
            return all((
                self.started_at.year == date.year,
                self.started_at.month == date.month,
                self.started_at.day > date.day
            ))


    @property
    def length(self) -> int:
        if not self.ended_at:
            return int((arrow.utcnow() - self.started_at).total_seconds())
        elif self.ended_at < self.started_at:
            return 0
        else:
            return int((self.ended_at - self.started_at).total_seconds())

    def __str__(self):
        return 'ID: {}, started: {}, ended: {}, length: {} seconds'.format(self._id, self.started_at, self.ended_at,
                                                                           self.length)

    def __repr__(self):
        return 'ID: {}, started: {}, ended: {}, length: {} seconds'.format(self._id, self.started_at, self.ended_at,
                                                                           self.length)
