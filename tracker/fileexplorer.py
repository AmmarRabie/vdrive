import sys
import zmq
from tokenanalyzer import TokenAnalyzer
from common.zmqHelper import zhelper
from appconfig import *

class FileExplorer:
    def __init__(self, serverPort):
        self.myPort = serverPort
        pass

    def explore(self):
        """
        synchronous(blocking) file exploring
        """
        socket = zhelper.newServerSocket(zmq.REP, TRACKER_IP, self.myPort)
        req = socket.recv_json()
        token = req.get("token")
        func = req.get("function")
        if (func != "ls"):
            print("Warning: file explorer receives a function that it is not a ls function")
            return
        userId = TokenAnalyzer.getUserId(token)
        if (not userId):
            print("file explorer receives a not valid token")
            return
        # files = db.getUserFiles(userId)
        filesNames = ("1.mp4", "miro.mp4", "45.mp4")
        socket.send_json({"files": filesNames})