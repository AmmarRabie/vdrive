"""
Run this file if you want a tracker process that deal with clients requests

paramaters to this script if be run directly:
1- port that the tracker node will bind for
"""
import sys
sys.path.append("../")
from fileexplorer import FileExplorer
from downloader import Downloader
from uploader import Uploader
from common.util import getCurrMachineIp, decodeToken
from common.zmqHelper import zhelper
from trackerdbcontroller import TrackerDBController as Db
import zmq

class ClientHandler:
    def __init__(self, port):
        ip = getCurrMachineIp()
        self.username, self.password = None, None
        self.socket = zhelper.newServerSocket(zmq.REP, ip, port)
        self.db = Db("TrackerDB")
        self.uploader = Uploader(self.socket, self.db)
        self.downloader = Downloader(self.socket, self.db)
        self.fileExplorer = FileExplorer(self.socket, self.db)
        
    def handleRequest(self):
        """
            syncrounous (blocking) function, waits until receiving an action, handle it and return
        """
        clientRequestInfo = self.socket.recv_json()
        userToken = clientRequestInfo.get("token")
        if not self._authenticate(userToken):
            print("authentication error")
            return
        
        function = clientRequestInfo.get("function")
        if function == "ls":
            self.fileExplorer.explore(self.socket, self.username)
        elif function == "download":
            fileName = clientRequestInfo.get("fileName")
            self.uploader.upload(fileName, self.username)
        elif function == "upload":
            self.downloader.download()
        else:
            print("not correct function: ", function, " should be one of 'download, upload, ls'")
            self.socket.send_string("Either you don't send a function or it is not a valid function")

    def _authenticate(self, userToken):
        if not userToken:
            print("no user token is supplied: ", userToken)
            self.socket.send_string("you should provide a token")
            return False
        self.username, self.password = decodeToken(userToken)
        if not self.username:
            print("can't decode the token: ", userToken)
            self.socket.send_string("Invalid token")
            return False
        return True


def main(port):
    clientHandler = ClientHandler(port)
    while(True):
        clientHandler.handleRequest()
        print("new request has been handled")

if __name__ == "__main__":
    import sys
    from appconfig import TRACKER_PORTS
    port = TRACKER_PORTS[0]
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    main(port)