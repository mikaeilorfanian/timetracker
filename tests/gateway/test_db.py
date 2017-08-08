import pickle
import os

from gateway import DB, DB_FILE_PATH


class TestMethodLoadsDBFileContentsIntoMemory:

    def test_db_file_is_created_when_it_doesnt_exist(self):
        try:
            os.remove(DB_FILE_PATH)
        except FileNotFoundError:
            pass

        DB(DB_FILE_PATH)
        assert os.path.exists(DB_FILE_PATH)

    def test_empty_db_is_returned_when_nothing_has_been_saved_in_it_yet(self):
        db = DB(DB_FILE_PATH)
        assert db.data == list()

    def test_db_content_is_returned_when_theres_something_in_it(self, test_activity):
        db = DB(DB_FILE_PATH)
        db.data = [test_activity]

        assert test_activity._id == db.data[0]._id
