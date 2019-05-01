import os
from appconfig import TRACKER_PORTS, TRACKER_PORTS_KEEPERS, PYTHON_PATH

os.chdir("./tracker")

for port in TRACKER_PORTS:
    os.system('start "tracker-client-{port}" {python} main_client.py {port}'.format(python=PYTHON_PATH, port=port))

port = 550550
print('start "tracker-datakeeper-{port}" {python} main_datakeeper.py {port}'.format(python=PYTHON_PATH, port=port))
for port in TRACKER_PORTS_KEEPERS:
    os.system('start "tracker-datakeeper-{port}" {python} main_datakeeper.py {port}'.format(python=PYTHON_PATH, port=port))


os.system('start "tracker-aliveReceiver" {python} aliveReceiver.py'.format(python=PYTHON_PATH))

os.system('start "tracker-replicator" {python} replicator.py'.format(python=PYTHON_PATH))

