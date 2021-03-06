from threading import Thread
import sys
import zmq
import pickle
import zlib
import progressbar
# sys.path.append("../common")
from common.util import writeVideo


class Downloader:
	
	def __init__(self, trackerIP="localhost", trackerPort=5000):
		self.trackerIP = trackerIP
		self.trackerPort = trackerPort
		
		
	def download_thread(self, ip, port, token, videoName, nodeIndex=6, totalNodes=6):
    	#create socket
		context = zmq.Context()
		socket = context.socket(zmq.REQ)
		socket.connect ("tcp://{}:{}".format(ip, port))
    
    	# send the metadata
		socket.send_json({
    		"function": "download",
    		"filename": videoName,
    		"token": token,
    		"config": f"{totalNodes} {nodeIndex}",
		})
    	# receive ack
		socket.recv_string()
    
    	#send to client number of chunks
		socket.send_string("GIVE ME THE CHUNKS")
		numberOfChunks = int(socket.recv_string())
    	#send ACK
		socket.send_string("ACK")


		#starting download
		video = []
		with progressbar.ProgressBar(max_value=numberOfChunks) as bar:
			for i in range(numberOfChunks):
				#receiving current chunk
				z = socket.recv_pyobj()
				#p = zlib.decompress(z)
				#s = pickle.loads(p)
				#print(type(s))
				video.append(z)

				#send ack
				socket.send_string("ACK")

				#update progress bar
				bar.update(i)
    
    	#finish
		message = socket.recv_string()
		print(message)
		self.video[nodeIndex] = video
    
    
	def getIPs(self, socket, token, videoName):
    	#send download request
		socket.send_json({
    		"token": token,
    		"function": "download",
    		"filename": videoName,
    	})
    
        # get ports and ips
		res = socket.recv_json()
		if 'err' in res.keys():
			print("error in downloader", "no ips available")
			return ''

		return res['ip_ports']
    
    
    
    # downloads a file from servers
    # ip_ports = [[ip, port], [ip, port], ...]
	def download(self, socket, token, videoName):
    	#get ip_ports
		ip_ports = self.getIPs(socket, token, videoName)
		if (not ip_ports):
			return False
		print(ip_ports)
    	#ip_ports = [["localhost", 7000], ["localhost", 7001], ["localhost", 7002], ["localhost", 7003], ["localhost", 7004]]
    	#list for download threads
		downloadThreads = []
    
    	# get number of nodes
		numNodes = len(ip_ports)
    
    	#downloadedVideo
		self.video = [None] * numNodes
    
    	#initialize threads
		for i in range(numNodes):
			args = ip_ports[i][0], ip_ports[i][1], token, videoName, i, numNodes
			thread = Thread(target=self.download_thread, args = args)
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
	video = downObj.download("1.mp4")
	writeVideo(video, "recv.mp4")