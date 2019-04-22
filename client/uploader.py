import zmq
from common.zmqHelper import zhelper
from appconfig import *
from common.util import readVideo
class Uploader:
    def __init__(self):
        pass

    def upload(self, socket, token = None, filePath = "client/vtest.mp4"):
        ip, port = self.requestUpload(socket, token)
        print("your file will be uploaded to ", ip + ":" + port)
        uploadSocket = zhelper.newSocket(zmq.REQ, ip, (port,))
        data = readVideo(filePath)
        filename = filePath.split("/")[-1]
        payload = {
            "function": "upload",
            "filename": filename,
            "numChunks": len(data),
        }
        if token:
            payload["token"] = token
        uploadSocket.send_json(payload)
        uploadSocket.recv()
        print("uploading start")
        for chunk in data:
            #? may want to send the token here also, network overhead
            uploadSocket.send(chunk)
            uploadSocket.recv()

    def requestUpload(self, trackerSocket, token):
        #send upload request
        trackerSocket.send_json({
            "token": token,
            "function": "upload",
		})

        # get ip:port for machine to communicate with
        connectionStr = trackerSocket.recv_string()
        return connectionStr.split(":", 1)
    def _sendChunk(self):
        pass