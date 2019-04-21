import sys
sys.path.append("../")
from threading import Thread
from common.zmqHelper import zhelper
from common.util import readVideo
import zmq
from appconfig import KEEPERS_TO_KEEPERS_REPL_PORTS as KEEPERS_TO_KEEPERS_PORTS, TRACKER_IP, TRACKER_PORTS
class ReplicatorSrc:
    def __init__(self, port):
        # self.trackerSocket = zhelper.newSocket()
        self.mysocket = zhelper.newServerSocket(zmq.REP, "*", port)

    def handleTrackerRequest(self):
        request = self.mysocket.recv_json()
        self.file, destinations = request.get("file"), request.get("dests")
        threads = []
        if(len(KEEPERS_TO_KEEPERS_PORTS) < len(destinations)):
            raise Exception("un-available state, do you forget to incremet number of KEEPERS_TO_KEEPERS_REPL_PORTS in appconfig ?")
        for i, dest in enumerate(destinations):
            t = Thread(target=self.replicate, args=(dest,i))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        self.mysocket.send_string("ACK") # ACK to the replicator process in the tracker to continue processing

    def replicate(self, dest, index):
        f = self.file
        print(f, dest)
        port = KEEPERS_TO_KEEPERS_PORTS[index]
        keeperSocket = zhelper.newSocket(zmq.REQ, dest["nodeIP"], (port,))
        uploader = Uploader()
        uploader.upload(keeperSocket, f["userID"], f["fileName"])


# OPTIMIZE TODO: remove this class and add the a general uploader in the common dir that can do client and replicator uploader 
class Uploader:
    def __init__(self):
        pass

    def upload(self, socket, username, filePath = "client/vtest.mp4"):
        data = readVideo(filePath)
        filename = filePath.split("/")[-1]
        payload = {
            "function": "upload",
            "username": username,
            "filename": filename,
            "numChunks": len(data),
        }
        socket.send_json(payload)
        socket.recv()
        print("uploading start")
        for chunk in data:
            socket.send(chunk)
            socket.recv()

def main(port):
    replicator = ReplicatorSrc(port)
    while(True):
        replicator.handleTrackerRequest()
        #? TODO: should we sleep here

if __name__ == "__main__":
    import sys
    from appconfig import TRACKER_TO_KEEPERS_PORTS
    port = TRACKER_TO_KEEPERS_PORTS[0]
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    main(port)