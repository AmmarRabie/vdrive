import sys
import zmq
sys.path.append("..")
from common.zmqHelper import zhelper
from sysconfig import TRACKER_IP, TRACKER_PORTS

class FileExplorer:
    def __init__(self):
        pass

    def explore(self, userId):
        """
        synchronous(blocking) file exploring
        """
        socket = zhelper.newSocket(zmq.REQ, TRACKER_IP, TRACKER_PORTS)
        socket.send_json({})
        files = socket.recv_json()
