import os

from .utils import load_db_into_memory


db_type = os.environ.get('DB_ENGINE', 'nosql')
app_env = os.environ.get('TIMETRACKER_APP_ENVIRONMENT', 'prod')


if app_env == 'test':
    db_name = 'timetracker_test_db'
else:
    db_name = 'timetracker_db'


DB_FILE_PATH = os.path.join(os.path.expanduser('~'), 'timetracker', db_name)


class Borg:
    _db = load_db_into_memory(DB_FILE_PATH)

    def __init__(self):
        self.__dict__ = self._db


class DB(Borg):
    def __init__(self):
        Borg.__init__(self)

    def __getitem__(self, x):
        return self.__dict__[x]

    def __setitem__(self, key, value):
        self.__dict__[key] = value


if db_type == 'nosql' and app_env == 'test':
    db = DB()
    db['activities'] = list()
