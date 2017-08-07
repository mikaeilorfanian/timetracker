import os

from .utils import load_db_into_memory


db_type = os.environ.get('DB_ENGINE', 'nosql')
app_env = os.environ.get('TIMETRACKER_APP_ENVIRONMENT', 'test')
db_name = os.environ.get('DB_FILE_NAME', 'timetracker_test_db')


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
