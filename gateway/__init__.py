from collections import defaultdict
import os

db_type = os.environ.get('DB_ENGINE', 'nosql')
app_env = os.environ.get('APP_ENVIRONMENT', 'test')


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class DB(Borg):
    def __init__(self):
        Borg.__init__(self)

    def __getitem__(self, x):
        return self.__dict__[x]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


if db_type == 'nosql' and app_env == 'test':
    db = DB()
    db['activities'] = defaultdict(list)
