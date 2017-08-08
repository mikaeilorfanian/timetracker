import os

from .utils import load_db_into_memory


app_env = os.environ.get('TIMETRACKER_APP_ENVIRONMENT', 'prod')


if app_env == 'test':
    db_name = 'timetracker_test_db'
else:
    db_name = 'timetracker_db'


DB_FILE_PATH = os.path.join(os.path.expanduser('~'), 'timetracker', db_name)


class DB:

    def __init__(self):
        self.__dict__ = load_db_into_memory(DB_FILE_PATH)

    def __getitem__(self, x):
        return self.__dict__[x]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def delete_db(self):
        try:
            os.remove(DB_FILE_PATH)
        except FileNotFoundError:
            pass
        self.__dict__ = load_db_into_memory(DB_FILE_PATH)
    def load_db_into_memory(self):
        if not os.path.exists(self.db_file_name):
            self.create_empty_db_file()

        with open(self.db_file_name, 'rb') as fp:
            return pickle.load(fp)

    def create_empty_db_file(self):
        os.makedirs(os.path.dirname(self.db_file_name), exist_ok=True)
        with open(self.db_file_name, 'wb') as fp:
            pickle.dump({'activities': list()}, fp)

