import sys
import zmq
from common.zmqHelper import zhelper
from appconfig import *

class FileExplorer:
    def __init__(self):
        pass

    def explore(self, userToken):
        """
        synchronous(blocking) file exploring
        """
        socket = zhelper.newSocket(zmq.REQ, TRACKER_IP, TRACKER_PORTS)
        socket.send_json({"token": userToken, "function": "ls"})
        files = socket.recv_json()
        print("my dear client, your files are: ", files)
