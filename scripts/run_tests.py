import prepare_for_tests

import subprocess
subprocess.run('pip install --editable .', shell=True)
subprocess.call('pytest')
