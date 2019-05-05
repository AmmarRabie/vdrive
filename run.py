import sys
import os
from appconfig import PYTHON_PATH

for arg in sys.argv[1:]:
    file = {"d": "runData.py", "m": "runDatabaseMaster.py", "s": "runSlave.py", "t": "runTracker.py"}.get(arg)
    if not file:
        print("not valid arg 'd s m t'")
        continue
    os.system('{python} {file}'.format(python=PYTHON_PATH, file=file))
