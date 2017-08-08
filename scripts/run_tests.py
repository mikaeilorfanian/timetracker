import argparse
import subprocess

import prepare_for_tests


parser = argparse.ArgumentParser()
parser.add_argument('--path', default='.', help='path to the specific test you want to run, runs all tests by default')
args = parser.parse_args()


subprocess.run('pip install --editable .', shell=True)
subprocess.call('pytest %s' % args.path, shell=True)
