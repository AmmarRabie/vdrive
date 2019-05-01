import os
from appconfig import TRACKER_PORTS, PYTHON_PATH

os.chdir("./tracker")

for port in TRACKER_PORTS:
    os.system('start "tracker-{port}" {python} main_client.py {port}'.format(python=PYTHON_PATH, port=port))

os.system('start "tracker-aliveReceiver" {python} aliveReceiver.py'.format(python=PYTHON_PATH))

os.system('start "tracker-replicator" {python} replicator.py'.format(python=PYTHON_PATH))

