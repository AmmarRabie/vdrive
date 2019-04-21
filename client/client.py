import zmq
from appconfig import TRACKER_IP, TRACKER_PORTS
from common.zmqHelper import zhelper
from common.util import generateToken, readVideo
import common.util as utils
from downloader import Downloader
from uploader import Uploader
from fileexplorer import FileExplorer

class Client:
    def __init__(self):
        self.socket = zhelper.newSocket(zmq.REQ, TRACKER_IP, TRACKER_PORTS)		
        self.downloader = Downloader()
        self.uploader = Uploader()
        self.fileExplorer = FileExplorer()

    def listFiles(self, token):
        files = self.fileExplorer.explore(self.socket, token)
        print("listFiles: files are")
        print("\n".join(files))
        return files

    def downloadFile(self, token, fileName, savePathDir = "."):
        downloadedFile = self.downloader.download(self.socket, token, fileName)
        utils.writeVideo(downloadedFile, f"{savePathDir}/{fileName}_rec.mp4")
        return downloadedFile
    
    def uploadLocalFile(self, token, filePath):
        return self.uploader.upload(self.socket, token, filePath)