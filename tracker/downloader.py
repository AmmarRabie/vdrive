"""
    send the port to the client
    don't run this file alone
"""
import zmq
import sys
import pickle
import zlib
sys.path.append("../common")
from util import readVideo
import random


class Downloader:
    def __init__(self, socket, db):
        # set refs
        self.socket = socket
        self.db = db

    def download(self):

        # make function atomic
        inUse = self.db.db.updateOne({"atomic": "atomic"}, {"inUse": True})["inUse"]
        while inUse:
            inUse = self.db.db.updateOne({"atomic": "atomic"}, {"inUse": True})["inUse"]

        emptyProcessesDB = self.db.getEmptyPortsAllMachines() # TODO: use this line instead of hard coded response
        # emptyProcesses = ["127.0.0.1:6000", "127.0.0.1:6000", "127.0.0.1:6000", "127.0.0.1:6000"]
        emptyProcesses = []
        for process in emptyProcessesDB:
            if self.db.isNodeAlive(process["nodeIP"]):
                emptyProcesses.append(f"{process['nodeIP']}:{process['port']}")

        # optimize: we can select the node with less files on that
        datakeeperChosen = emptyProcesses[random.randint(0, len(emptyProcesses) - 1)]

        #set busy
        self.db.setNodeBusyState(datakeeperChosen["nodeIP"], datakeeperChosen["port"], True)

        # free atomic
        self.db.db.updateOne({"atomic": "atomic"}, {"inUse": False})["inUse"]
        
        # send the connection string
        self.socket.send_string(datakeeperChosen)