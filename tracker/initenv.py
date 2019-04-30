'''
    init the env of mongo
'''
from trackerdbcontroller import TrackerDBController as Db
import sys
sys.path.append("../")
from appconfig import DATA_KEEPER_IPS, DATA_KEEPER_PORTS
def main():
    db = Db("TrackerDB")
    for ip in DATA_KEEPER_IPS:
        db.insertNode(ip, ports=DATA_KEEPER_PORTS)

if __name__ == "__main__":
    main()