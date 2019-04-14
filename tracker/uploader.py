import zmq
import sys
import pickle
import zlib
sys.path.append("../common")
from util import readVideo



class Uploader:
    

    def __init__(self, port=6555):
    	self.port = port


    def upload(self, path):

    	#create socket
    	context = zmq.Context()
    	socket = context.socket(zmq.REP)
    	socket.bind("tcp://*:%s" % self.port)

    	#read video
    	video = readVideo(path)

    	#recieve total length and self index
    	config = socket.recv_string()

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
    	socket.send_string(str(numberOfChunks))

    	#get ACK
    	ack = socket.recv_string()

    	print(len(video))

    	#start uploading
    	for i in range(selfIndex * numberOfChunksOriginal, selfIndex * numberOfChunksOriginal + numberOfChunks):
    	    #sending current chunk
    	    #print(type(video[i]))
    	    #p = pickle.dumps(video[i])
    	    #z = zlib.compress(p)
    	    socket.send_pyobj(video[i])

    	    #get ack
    	    ack = socket.recv_string()

    	#finish
    	socket.send_string("Finish Chunk :D")
    	print("Finish Chunk :D")


if __name__ == '__main__':
	upObj = Uploader()
	upObj.upload("dummyvideo.mp4")