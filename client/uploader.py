import zmq
from common.zmqHelper import zhelper
from appconfig import *
from common.util import readVideo
import progressbar
class Uploader:
    def __init__(self):
        pass

    def upload(self, socket, token = None, filePath = "client/vtest.mp4"):
        ip, port = self.requestUpload(socket, token)
        if (not ip):
            return False
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
        with progressbar.ProgressBar(max_value=len(data)) as bar:
            for i in range(len(data)):
                #? may want to send the token here also, network overhead
                uploadSocket.send(data[i])
                uploadSocket.recv()

                #update progress bar
                bar.update(i)

    def requestUpload(self, trackerSocket, token):
        #send upload request
        trackerSocket.send_json({
            "token": token,
            "function": "upload",
		})

        # get ip:port for machine to communicate with
        response = trackerSocket.recv_json()
        if 'err' in response.keys():
            print(response['err'])
            return '', ''
        connectionStr = response['connectionStr']
        return connectionStr.split(":", 1)
    def _sendChunk(self):
        pass