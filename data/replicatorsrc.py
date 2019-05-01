import sys
sys.path.append("../")
from threading import Thread
from common.zmqHelper import zhelper
from common.util import readVideo
import zmq
import progressbar
from appconfig import KEEPERS_TO_KEEPERS_REPL_PORT as KEEPERS_TO_KEEPERS_PORT, TRACKER_IP, TRACKER_PORTS
class ReplicatorSrc:
    def __init__(self, port):
        # self.trackerSocket = zhelper.newSocket()
        self.mysocket = zhelper.newServerSocket(zmq.REP, "*", port)

    def handleTrackerRequest(self):
        request = self.mysocket.recv_json()
        self.file, destinations = request.get("file"), request.get("dests")
        threads = []
        for dest in destinations:
            t = Thread(target=self.replicate, args=(dest,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print("sending to the tracker to continue replication")
        self.mysocket.send_string("ACK") # ACK to the replicator process in the tracker to continue processing

    def replicate(self, dest):
        f = self.file
        print(f, dest)
        port = KEEPERS_TO_KEEPERS_PORT
        keeperSocket = zhelper.newSocket(zmq.REQ, dest["nodeIP"], (port,))
        uploader = Uploader()
        uploader.upload(keeperSocket, f["userID"], f["fileName"])


# OPTIMIZE TODO: remove this class and add the a general uploader in the common dir that can do client and replicator uploader 
# OPTIMIZE TODO: read the file only one before opening the threads

class Uploader:
    def __init__(self):
        pass

    def upload(self, socket, username, filename):
        data = readVideo(f"{username}/{filename}")
        payload = {
            "function": "upload",
            "username": username,
            "filename": filename,
            "numChunks": len(data),
        }
        socket.send_json(payload)
        socket.recv()
        print("uploading start")
        with progressbar.ProgressBar(max_value=len(data)) as bar:
            for i in range(len(data)):
                socket.send(data[i])
                socket.recv()
                bar.update(i)

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
