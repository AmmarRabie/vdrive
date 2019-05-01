"""
    For the client who wants to download, send the not busy alive ports that have this file
"""

import zmq
import sys
import pickle
import zlib
sys.path.append("../common")
from util import readVideo
from util import decodeToken



class Uploader:
    def __init__(self, socket, db):
        self.socket = socket
        self.db = db
        self.numPorts = 6


    def upload(self, fileName, userId):

        # make function atomic
        inUse = self.db.db.updateOne({"atomic": "atomic"}, {"inUse": True})["inUse"]
        while inUse:
            inUse = self.db.db.updateOne({"atomic": "atomic"}, {"inUse": True})["inUse"]

        # get nodes containing the file
        nodes = self.db.getPortsForDownload(userId, fileName)

        print(nodes)

        if len(nodes) != 0:
            IP_Ports = []

            # number of appended ports
            i = 0
            # current port
            j = 0
            errors = 0
            while i < self.numPorts and errors < len(nodes):
                errors = 0
                for node in nodes:
                    try:
                        ip_port = [node[0], node[1][j]]
                        IP_Ports.append(ip_port)
                        i += 1
                        self.db.setNodeBusyState(ip_port[0], ip_port[1], True)
                    except IndexError:
                        errors += 1
                j += 1

        else:
            print("WARNING: upload can't find a given file name on any nodes (may be the file name is not true)")
            IP_Ports = []

        # free atomic
        self.db.db.updateOne({"atomic": "atomic"}, {"inUse": False})["inUse"]

        # send ports and ips
        self.socket.send_pyobj(IP_Ports[:self.numPorts])



if __name__ == '__main__':
	upObj = Uploader()
	upObj.upload()