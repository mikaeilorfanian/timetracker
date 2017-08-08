import os

from .utils import load_db_into_memory


app_env = os.environ.get('TIMETRACKER_APP_ENVIRONMENT', 'prod')


if app_env == 'test':
    db_name = 'timetracker_test_db'
else:
    db_name = 'timetracker_db'


DB_FILE_PATH = os.path.join(os.path.expanduser('~'), 'timetracker', db_name)


class DB:

    def __init__(self, db_file_name):
        self.db_file_name = db_file_name
        self._in_memory_db = self.load_db_into_memory()

    @property
    def data(self):
        return self.load_db_into_memory()['activities']

    @data.setter
    def data(self, new_data):
        self._in_memory_db = {'activities': new_data}
        self.commit()


    def delete_db(self):
        try:
            os.remove(DB_FILE_PATH)
        except FileNotFoundError:
            pass

    def commit(self):
        with open(self.db_file_name, 'wb') as fp:
            pickle.dump(self._in_memory_db, fp)

    def load_db_into_memory(self):
        if not os.path.exists(self.db_file_name):
            self.create_empty_db_file()

        with open(self.db_file_name, 'rb') as fp:
            return pickle.load(fp)

    def create_empty_db_file(self):
        os.makedirs(os.path.dirname(self.db_file_name), exist_ok=True)
        with open(self.db_file_name, 'wb') as fp:
            pickle.dump({'activities': list()}, fp)

