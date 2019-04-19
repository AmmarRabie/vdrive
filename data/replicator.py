import sys
sys.path.append("../")
from threading import Thread
from common.zmqHelper import zhelper
import zmq
from appconfig import KEEPERS_TO_KEEPERS_REPL_PORTS as KEEPERS_TO_KEEPERS_PORTS, TRACKER_IP, TRACKER_PORTS
from uploader import Uploader
class Replicator:
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
        self.mysocket.send_string("ACK") # ACK

    def replicate(self, dest, index):
        print(self.file, dest)
        trackerSocket = zhelper.newSocket(zmq.REQ, TRACKER_IP, (TRACKER_PORTS[0],))
        port = KEEPERS_TO_KEEPERS_PORTS[index]
        keeperSocket = zhelper.newSocket(zmq.REQ, dest["IP"], (port,))
        uploader = Uploader(keeperSocket, trackerSocket)
        # uploader.upload({
        #     "filename": file[""]
        # })
        pass

def main(port):
    replicator = Replicator(port)
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
