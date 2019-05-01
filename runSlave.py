import os
from appconfig import PYTHON_PATH

os.chdir("./database")

os.system('start "database-slave" {python} slave.py'.format(python=PYTHON_PATH))