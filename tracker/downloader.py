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
        inUse = self.db.db.findAndUpdate({"atomic": "atomic"}, {"inUse": True})["inUse"]
        print("inUse", inUse)
        while inUse:
            inUse = self.db.db.findAndUpdate({"atomic": "atomic"}, {"inUse": True})["inUse"]

        emptyProcessesDB = self.db.getEmptyPortsAllMachines() # TODO: use this line instead of hard coded response
        # emptyProcesses = ["127.0.0.1:6000", "127.0.0.1:6000", "127.0.0.1:6000", "127.0.0.1:6000"]
        emptyProcesses = []
        for process in emptyProcessesDB:
            if self.db.isNodeAlive(process["nodeIP"]):
                emptyProcesses.append(f"{process['nodeIP']}:{process['port']}")

        # optimize: we can select the node with less files on that
        print(f"we have {len(emptyProcesses)} available for download")
        if (not emptyProcesses):
            self.socket.send_json({"err": "no available ports"}) # TODO: handle this from the client
            self.db.db.updateOne({"atomic": "atomic"}, {"inUse": False})
            return
        datakeeperChosen = emptyProcesses[random.randint(0, len(emptyProcesses) - 1)]

        #set busy
        ip, port = datakeeperChosen.split(":")
        self.db.setNodeBusyState(ip, port, True)

        # free atomic
        self.db.db.updateOne({"atomic": "atomic"}, {"inUse": False})
        
        # send the connection string
        self.socket.send_string(datakeeperChosen)