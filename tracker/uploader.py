import zmq
import sys
import pickle
import zlib
from trackerdbcontroller import TrackerDBController
sys.path.append("../common")
from util import readVideo



class Uploader:
    

    def __init__(self, port=5000, dbname="TrackerDB"):
        self.port = port

        #create socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % self.port)

        #connect to database
        self.dbController = TrackerDBController(dbname)

        #ports to use for download
        self.downloadPorts = [6000, 6001, 6002, 6003, 6004, 6005]


    def upload(self):

        while(True):
            #recieve file name
            fileName = self.socket.recv_string()

            #get nodes containing the file
            nodes = self.dbController.getFileNodes(fileName)

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
                IP_Ports = []

            #send ports and ips
            self.socket.send_pyobj(IP_Ports)



if __name__ == '__main__':
	upObj = Uploader()
	upObj.upload()