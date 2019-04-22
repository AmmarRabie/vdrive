"""
    Run this file if you want a process on data keeper which handles the clinets requests
    client requests should be one of the following
        • download: client wants to download a given file, json sent should have metadata of the filename, userid, numChunks, config
        • upload: client wants to upload a file, json send should have metadata of username, filename, numChunks
"""
import sys
sys.path.append("../")
import zmq
from downloader import Downloader
from uploader import Uploader
from common.zmqHelper import zhelper
from common.util import getCurrMachineIp, decodeToken
from appconfig import TRACKER_IP, TRACKER_PORTS_KEEPERS
def main(port):
    #? TODO: when to use udp protocol
    trackerSocket = zhelper.newSocket(zmq.REQ, TRACKER_IP, TRACKER_PORTS_KEEPERS)
    downloadUploadSocket = zhelper.newServerSocket(zmq.REP, getCurrMachineIp(), port)
    downloader = Downloader(downloadUploadSocket, trackerSocket, port)
    uploader = Uploader(downloadUploadSocket, trackerSocket)
    while True:
        request = downloadUploadSocket.recv_json()
        print("request received:", request)
        username = authenticate(downloadUploadSocket, request.get("token"))
        downloadUploadSocket.send_string("ACK")
        if not username:
            continue
        del request["token"]
        request["username"] = username
        if request.get("function") == "download":
            uploader.upload(request)
        elif request.get("function") == "upload":
            downloader.download(request)

def authenticate(socket, userToken):
    if not userToken:
        socket.send_string("you should provide a token")
        return ""
    username, _ = decodeToken(userToken)
    if not username:
        socket.send_string("Invalid token")
        return ""
    return username

if __name__ == "__main__":
    from appconfig import DATA_KEEPER_PORTS
    port = DATA_KEEPER_PORTS[0]
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    main(port)
    pass