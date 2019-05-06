import sys
import zmq
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
        filesNames = self.db.getUserFiles(userId)
        print(f"tracker/FileExplorer: files of the user {userId} will be sent, they are: {filesNames}")
        self.socket.send_json({"files": filesNames})