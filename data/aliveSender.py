import sys
sys.path.append("../")
from common.zmqHelper import zhelper
import zmq
import time
from common.util import getCurrMachineIp
from appconfig import TRACKER_ALIVE_PORT as ALIVE_PORT, DATA_KEEPER_ALIVE_SEND_RATE as SEND_RATE

class AliveSender:
    def __init__(self):
        self.ip = getCurrMachineIp()
        self.socket = zhelper.newServerSocket(zmq.PUB, self.ip, ALIVE_PORT)

    def update(self):
        self.socket.send_string(f"{self.ip} :)")
        
if __name__ == "__main__":
    aliveSender = AliveSender()
    while(True):
        aliveSender.update()
        #? should we run this update method with delay so that not to consume processor power
        time.sleep(SEND_RATE)