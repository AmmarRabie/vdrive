import os
from appconfig import DATA_KEEPER_PORTS, PYTHON_PATH, TRACKER_ALIVE_PORT

os.chdir("./data")

for port in DATA_KEEPER_PORTS:
    os.system('start "data-{port}" {python} clienthandler.py {port}'.format(python=PYTHON_PATH, port=port))


os.system('start "data-alive-sender" {python} aliveSender.py'.format(python=PYTHON_PATH, port=port))

os.system('start "data-replicator-src" {python} replicatorsrc.py'.format(python=PYTHON_PATH))
os.system('start "data-replicator-dst" {python} replicatordst.py'.format(python=PYTHON_PATH, port=port))
