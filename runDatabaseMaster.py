import os
from appconfig import PYTHON_PATH

os.chdir("./database")

os.system('start "database-master" {python} master.py'.format(python=PYTHON_PATH))