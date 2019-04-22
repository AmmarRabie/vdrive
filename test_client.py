import os

PYTHON_PATH = "D:/workspace/TYFDS/venv/Scripts/python.exe"
print("start {python} client 8080".format(python=PYTHON_PATH))
os.system("start {python} client 8080".format(python=PYTHON_PATH))
os.chdir("./tracker")
os.system("start {python} main_client.py 7000".format(python=PYTHON_PATH))
os.chdir("../data")
os.system("start {python} clienthandler.py 6000 & pause".format(python=PYTHON_PATH))
