import zmq
import sys
import pickle
import zlib
from threading import Thread
sys.path.append("../common")
from util import readVideo



class Uploader:
    

    def __init__(self, port=6555):
    	self.port = port
    	#create socket
    	self.context = zmq.Context()
    	self.socket = self.context.socket(zmq.REP)
    	self.socket.bind("tcp://*:%s" % self.port)


    def upload(self):

    	#recieve the video name
    	videoName = self.socket.recv_string()

    	#send ack
    	self.socket.send_string("ACK")

    	#read video
    	video = readVideo(videoName)

    	#recieve total length and self index
    	config = self.socket.recv_string()

    	#extract total number of nodes and self index
    	config = config.split(" ")
    	numNodes = int(config[0])
    	selfIndex = int(config[1])

    	#calculate number of chunks to be sent
    	numberOfChunksOriginal = int(len(video) * 1.0 / numNodes)
    	numberOfChunks = numberOfChunksOriginal
    	if selfIndex == numNodes - 1:
    		numberOfChunks += + len(video) % numNodes

    	#send to client number of chunks
    	self.socket.send_string(str(numberOfChunks))

    	#get ACK
    	ack = self.socket.recv_string()

    	print(len(video))

    	#start uploading
    	for i in range(selfIndex * numberOfChunksOriginal, selfIndex * numberOfChunksOriginal + numberOfChunks):
    	    #sending current chunk
    	    #print(type(video[i]))
    	    #p = pickle.dumps(video[i])
    	    #z = zlib.compress(p)
    	    self.socket.send_pyobj(video[i])

    	    #get ack
    	    ack = self.socket.recv_string()

    	#finish
    	self.socket.send_string("Finish :D")
    	print("Finish :D")


if __name__ == '__main__':
	upObj = Uploader(sys.argv[1])
	upObj.upload()