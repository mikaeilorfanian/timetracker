import arrow


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
