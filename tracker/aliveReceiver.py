"""
    run this file if you want a receiver process from data keepers
"""


import sys
sys.path.append("../")
from common.zmqHelper import zhelper
import zmq
import time
from trackerdbcontroller import TrackerDBController as Db
from appconfig import DATA_KEEPER_IPS, TRACKER_ALIVE_PORT as ALIVE_PORT, DATA_KEEPER_TIME_OUT



class AliveReceiver:
    def __init__(self):
        s = zhelper.newSocketMultiIps(zmq.SUB, DATA_KEEPER_IPS, ALIVE_PORT)
        s.setsockopt(zmq.RCVTIMEO, 300)
        for ip in DATA_KEEPER_IPS:
            s.subscribe(ip)
        self.socket = s
        self.db = Db("TrackerDB")

    
    def update(self):
        isAliveStates = {}
        # init all with dead
        for ip in DATA_KEEPER_IPS:
            isAliveStates[ip] = False
        
        currentTime = time.time()
        endTime = currentTime + DATA_KEEPER_TIME_OUT
        while time.time() < endTime:
            try:
                senderIp, _ = self.socket.recv_string().split(" ", 1) # here is topic which is the ip and the message we don't care about
                isAliveStates.update({senderIp: True})
            except zmq.ZMQError as e:
                print("error while receiving: ", e)
                pass
        # OPTIMIZE: TODO, we may update the difference only
        print("updating with: ", isAliveStates)
        self.db.updateNodesAliveStates(isAliveStates)


if __name__ == "__main__":
    aliveReceiver = AliveReceiver()
    while(True):
        aliveReceiver.update()
        #? should we run this update method with delay so that not to consume processor power
        # time.sleep()