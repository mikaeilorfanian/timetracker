import os

db_type = os.environ.get('DB_ENGINE', 'nosql')
app_env = os.environ.get('APP_ENVIRONMENT', 'test')

if db_type == 'nosql' and app_env == 'test':
    db = dict()
