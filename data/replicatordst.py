import sys
sys.path.append("../")
from threading import Thread
from common.zmqHelper import zhelper
from common.util import writeVideo, getCurrMachineIp
import zmq
from appconfig import TRACKER_IP, TRACKER_PORTS_KEEPERS
class ReplicatorDst:
    def __init__(self, port):
        # self.trackerSocket = zhelper.newSocket()
        self.mysocket = zhelper.newServerSocket(zmq.REP, "*", port)
        trackerSocket = zhelper.newSocket(zmq.REQ, TRACKER_IP, TRACKER_PORTS_KEEPERS)
        self.downloader = Downloader(self.mysocket, trackerSocket, port)

    def handleKeeperRequest(self):
        request = self.mysocket.recv_json()
        self.mysocket.send_string("ACK")
        self.downloader.download(request)

# OPTIMIZE TODO: remove this class and add the a general uploader in the common dir that can do client and replicator uploader 
class Downloader:
    def __init__(self, socket, trackerSocket, port):
        self.socket = socket
        self.trackerSocket = trackerSocket
        self.myport = port
        

    def download(self, metadata): # client upload a video to this node
        # =================================================================================
        #   1- [passed as a parameter]: receive the meta data of the file ==> username, filename, chunks numbers 
        #   2- receive chunk by chunk
        #   3- write the file data under ./username/filename.mp4
        #   4- send the success message to the client
        #   5- send the success message to the tracker to free this port
        # =================================================================================
        username, filename, numChunks = metadata.get("username"), metadata.get("filename"), metadata.get("numChunks")
        print(f"receiving file: {filename} for user: {username}")

    	#start downloading
        vidData = []
        for _ in range(numChunks - 1):
            chunk = self.socket.recv()
            #send ack
            self.socket.send_string("ACK")
            vidData.append(chunk)
        chunk = self.socket.recv()
        vidData.append(chunk)

        # write the video on the machine disk under this user dir
        writeVideo(vidData, f"{username}/{filename}")
        
        # till the tracker that process is done to update the database
        self.trackerSocket.send_json({ # TODO function download at the tracker will free this port, we can make use of already busy strategy implemented
            "function": "download",
            "filename": filename,
            "username": username,
            "ip": getCurrMachineIp(),
            "port": self.myport
        })
        _ = self.trackerSocket.recv()

        #send success to the src Keeper
        self.socket.send_string("SUCCESS")

        

def main(port):
    replicator = ReplicatorDst(port)
    while(True):
        replicator.handleKeeperRequest()
        #? TODO: should we sleep here

if __name__ == "__main__":
    from appconfig import KEEPERS_TO_KEEPERS_REPL_PORT as port
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    main(port)
