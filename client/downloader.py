from threading import Thread
import sys
import zmq
import pickle
import zlib
sys.path.append("../common")
from util import writeVideo


class Downloader:
    
    def __init__(self):
    	pass


    def download_thread(self, ip, port, nodeIndex=6, totalNodes=6):
    	#create socket
    	context = zmq.Context()
    	socket = context.socket(zmq.REQ)
    	socket.connect ("tcp://{}:{}".format(ip, port))

    	# video collected
    	video = []

    	#send total length and node index
    	socket.send_string("{} {}".format(totalNodes, nodeIndex))

    	#send to client number of chunks
    	numberOfChunks = int(socket.recv_string())

    	#send ACK
    	socket.send_string("ACK")

    	#start downloading
    	for i in range(numberOfChunks):
    		#recieving current chunk
    		z = socket.recv_pyobj()
    		#p = zlib.decompress(z)
    		#s = pickle.loads(p)
    		#print(type(s))
    		video.append(z)

    		#send ack
    		socket.send_string("ACK")

    	#finish
    	message = socket.recv_string()
    	print(message)
    	return video

    

    def download(self, ips_dict):
    	pass


if __name__ == '__main__':
	downObj = Downloader()
	video = downObj.download_thread("localhost", 6555, 0, 1)
	writeVideo(video, "dummy.mp4")