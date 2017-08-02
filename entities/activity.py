

class Activity:
    STARTED = 'started'
    ENDED = 'ended'

    def __init__(self, category):
        self.status = None
        self.category = category

    def start(self):
        self.status = self.STARTED

    def end(self):
        self.status = self.ENDED

    @property
    def started(self):
        return self.status == self.STARTED

    @property
    def ended(self):
        return self.status == self.ENDED
