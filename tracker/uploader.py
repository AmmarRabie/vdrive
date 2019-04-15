import zmq
import sys
import pickle
import zlib
from trackerdbcontroller import TrackerDBController
sys.path.append("../common")
from util import readVideo



class Uploader:
    

    def __init__(self, port=5000, dbname="TrackerDB"):
    	self.port = port

        #create socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % self.port)

        #connect to database
        self.dbController = TrackerDBController(dbname)


    def upload(self, path):
        #recieve file name



if __name__ == '__main__':
	upObj = Uploader()
	upObj.upload("dummyvideo.mp4")