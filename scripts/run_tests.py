import os


os.environ['DB_ENGINE'] = 'nosql'
os.environ['TIMETRACKER_APP_ENVIRONMENT'] = 'test'


import subprocess
subprocess.run('pip install --editable .', shell=True)
subprocess.call('pytest')
