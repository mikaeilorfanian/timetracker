import os


os.environ['DB_ENGINE'] = 'nosql'
os.environ['TIMETRACKER_APP_ENVIRONMENT'] = 'test'


import subprocess
subprocess.call('pytest')
