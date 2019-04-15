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
    	self.video[nodeIndex] = video


    def getIPs(self, videoName):
    	

    
    # downloads a file from servers
    # ip_ports = [[ip, port], [ip, port], ...]
    def download(self, ip_ports):
    	#list for download threads
    	downloadThreads = []

    	# get number of nodes
    	numNodes = len(ip_ports)

    	#downloadedVideo
    	self.video = [None] * numNodes

    	#initialize threads
    	for i in range(numNodes):
    		thread = Thread(target=self.download_thread(ip_ports[i][0], ip_ports[i][1], i, numNodes))
    		downloadThreads.append(thread)

    	# start threads
    	for thread in downloadThreads:
    		thread.start()

    	# join threads
    	for thread in downloadThreads:
    		thread.join()

    	#create final video
    	finalVideo = []
    	for chunk in self.video:
    		for element in chunk:
    			finalVideo.append(element)

    	return finalVideo




if __name__ == '__main__':
	downObj = Downloader()
	video = downObj.download([["localhost", 6555], ["localhost", 6556], ["localhost", 6557], ["localhost", 6558]])
	writeVideo(video, "dummy.mp4")