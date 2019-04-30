import os
from appconfig import DATA_KEEPER_PORTS


PYTHON_PATH = "D:/workspace/TYFDS/venv/Scripts/python.exe"
os.chdir("./data")

for port in DATA_KEEPER_PORTS:
    os.system("start {python} clienthandler.py {port}".format(python=PYTHON_PATH, port=port))
