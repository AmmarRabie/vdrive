
from common.util import writeVideo, getCurrMachineIp

class Downloader:
    def __init__(self, socket, trackerSocket, port):
        self.socket = socket
        self.trackerSocket = trackerSocket
        self.myport = port
        

    def download(self, metadata): # client upload a video to this node
        # =================================================================================
        #   1- [passed as a parameter]: receive the meta data of the file ==> username, filename, chunks numbers 
        #   2- receive chunk by chunk
        #   3- write the file data under ./username/filename.mp4
        #   4- send the success message to the client
        #   5- send the success message to the tracker to free this port
        # =================================================================================
        username, filename, numChunks = metadata.get("username"), metadata.get("filename"), metadata.get("numChunks")

    	#send ack
        # self.socket.send_string("ACK")

    	#start downloading
        vidData = []
        for _ in range(numChunks - 1):
            chunk = self.socket.recv()
            #send ack
            self.socket.send_string("ACK")
            vidData.append(chunk)
        chunk = self.socket.recv()
        vidData.append(chunk)

        # write the video on the machine disk under this user dir
        writeVideo(vidData, f"{username}/{filename}")
        
        # till the tracker that process is done to update the database
        self.trackerSocket.send_json({
            "function": "download",
            "filename": filename,
            "username": username,
            "ip": getCurrMachineIp(),
            "port": self.myport
        })
        _ = self.trackerSocket.recv()

        #send success to the client
        self.socket.send_string("SUCCESS")

        


if __name__ == '__main__':
	upObj = Uploader(sys.argv[1])
	upObj.upload()