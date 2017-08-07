import pickle
import os


def load_db_into_memory(db_file_path):
    if not os.path.exists(db_file_path):
        create_empty_db_file(db_file_path)

    with open(db_file_path, 'rb') as fp:
        return pickle.load(fp)


def create_empty_db_file(db_file_path):
    os.makedirs(os.path.dirname(db_file_path), exist_ok=True)
    with open(db_file_path, 'wb') as fp:
        pickle.dump({'activities': list()}, fp)
