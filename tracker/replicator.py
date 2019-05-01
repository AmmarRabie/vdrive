import sys
sys.path.append("../")
import time
import zmq
from trackerdbcontroller import TrackerDBController
from common.zmqHelper import zhelper
from appconfig import TRACKER_TO_KEEPERS_PORTS as KEEPERS_PORTS

MIN_REPLICATION = 3
class Replicator:
    dbManager = None
    maximumFilesOnNode = 0
    filesLocations = []
    nodesStates = {}

    def __init__(self, dbname="TrackerDB"):
        self.db = TrackerDBController(dbname)

    def replicator_process(self):       
        listOfFiles = self.db.listAllFilesAllUsers()
        listOfNodes = self.db.listAliveNodes()
        print("listOfFiles", listOfFiles)

        listOfNodes = sorted(listOfNodes, key=lambda k: k["numFiles"]) #, reverse=True) 
        print("listOfNodes=", listOfNodes)
    
        for file in listOfFiles:
            print("handling file:", file)

            # instances = (sum(value["fileName"] == file["fileName"] for value in filesLocations))
            # TODO: we don't need this function: we will get the number of instances from getting the len(src)
            instances = self.db.getInstancesOfFile(file["userID"],file["fileName"])

            src = next((item for item in listOfNodes if item["nodeID"] == file["nodeID"]), None)
            # instances = len(src)
            if not src:
                print("OH MY GOD, this file can't be replicated as the whole src nodes are died")
                continue
            requiredDestNum = MIN_REPLICATION - instances
            if (requiredDestNum <= 0):
                continue

            print("src = ", src, f"should be transferred to {requiredDestNum} machines")

            destinations = (item for item in listOfNodes if ( item != src ) and not self.db.isFileOnNode(file["fileName"], item["nodeIP"], file["userID"]))
            availableNodesNum = len(destinations)
            if (availableNodesNum < requiredDestNum):
                print(f"there is only {availableNodesNum} nodes, but {requiredDestNum} required")
            selectedMachines = destinations[:max(availableNodesNum, requiredDestNum)]

            
            print("selectedMachines=", selectedMachines)
            srcSocket = zhelper.newSocket(zmq.REQ, src, KEEPERS_PORTS)
            srcSocket.send_json({
                "dests": selectedMachines,
                "file": file
            })
            srcSocket.recv() # ack that replication has been done

if __name__ == '__main__':
    replicatorObject = Replicator("TrackerDB")
    while(True):
        replicatorObject.replicator_process()
        time.sleep(5)