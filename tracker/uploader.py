"""
    For the client who wants to download, send the not busy alive ports that have this file
"""

import zmq
import sys
import pickle
import zlib
sys.path.append("../common")
from util import readVideo



class Uploader:
    def __init__(self, socket, db):
        self.socket = socket
        self.db = db
        
        # TODO: remove this line, this data will received while upload function
        self.downloadPorts = (6000, 6001, 6002, 6003, 6004, 6005)


    def upload(self, fileName, userId):
        # TODO: implement the logic of getting ips-ports to include the busy strategy
        #get nodes containing the file
        nodes = self.db.getFileNodes(fileName)

        print(nodes)

        if len(nodes) != 0:
            #get ports per node
            portsPerNode = int(len(self.downloadPorts) / len(nodes))

            # make IP Ports list
            IP_Ports = []
            for node in nodes:
                for i in range(portsPerNode):
                    IP_Ports.append([node["IP"], self.downloadPorts[i]])

            #add the rest of ports
            for i in range(len(self.downloadPorts) % len(nodes)):
                IP_Ports.append([nodes[i]["IP"], self.downloadPorts[portsPerNode]])
        else:
            print("WARNING: upload can't find a given file name on any nodes (may be the file name is not true)")
            IP_Ports = []

        #send ports and ips
        self.socket.send_pyobj(IP_Ports)



if __name__ == '__main__':
	upObj = Uploader()
	upObj.upload()