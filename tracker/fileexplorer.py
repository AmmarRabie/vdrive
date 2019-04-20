import sys
import zmq
from tokenanalyzer import TokenAnalyzer
from common.zmqHelper import zhelper
from appconfig import *


class FileExplorer:
    def __init__(self, socket, db):
        self.db = db
        self.socket = socket

    def explore(self, socket, userId):
        if (not userId):
            print("WARNING: file explorer receives a not valid userId")
            return
        # files = self.db.getUserFiles(userId)
        filesNames = ("1.mp4", "miro.mp4", "45.mp4") # TODO: Get it from the database
        print(f"files of the user {userId} will be sent, they are: {filesNames}")
        self.socket.send_json({"files": filesNames})