import sys
import zmq
from common.zmqHelper import zhelper
from appconfig import TRACKER_IP, TRACKER_PORTS

class FileExplorer:
    def __init__(self):
        pass

    def explore(self, socket, token):
        """
        synchronous(blocking) file exploring
        """
        socket.send_json({"token": token, "function": "ls"})
        files = socket.recv_json()
        return files.get("files")
        # print("my dear client, your files are: ", files)
