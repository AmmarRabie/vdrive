# import tracker.__main__ as tracker
# import 

# tracker.main()

import os
from appconfig import TRACKER_PORTS

for port in TRACKER_PORTS:
    os.system(f"start python tracker {port}")