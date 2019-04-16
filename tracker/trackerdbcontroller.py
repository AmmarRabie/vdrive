import sys
sys.path.append('../common')
from dbmanager import DBManager


class TrackerDBController:

	def __init__(self, dbname, host='localhost', port='27017'):
		self.db = DBManager(dbname)


	#used for ls command
	def getUserFiles(self, userID):
		files = self.db.retrieveAll({"userID": userID})
		fileNames = []
		for item in files:
			fileNames.append(files["fileName"])
		return fileNames


	#returns True if node is alive and False if not
	def isNodeAlive(self, nodeID):
		return self.db.retrieveOne({"nodeID": nodeID})["alive"]


	#return the number of files on the node
	def getNodeNumberOfFiles(self, nodeID):
		return self.db.retrieveOne({"nodeID": nodeID})["numFiles"]


	#returns alive nodes IDs where the file is there
	def getFileNodes(self, fileName):
		nodesIDs = self.db.retrieveAll({"fileName": fileName})
		aliveNodes = []
		for item in nodesIDs:
			if self.isNodeAlive(item["nodeID"]):
				aliveNodes.append(item["nodeID"])
		return aliveNodes


	#insert a file for a specefic user
	def insertFile(self, userID, fileName):
		self.db.insertOne({"userID": userID, "fileName": fileName})


	#make the node alive or not
	#alive is a bool variable
	def setNodeState(self, nodeID, alive):
		self.db.updateOne({"nodeID": nodeID}, {"alive": alive})


	#add file to a node
	def addFileToNode(self, fileName, nodeID):
		self.db.insertOne({"fileName": fileName}, {"nodeID": nodeID})


	#adds a machine node to the system
	def insertNode(self, nodeID, numFiles=0, alive=True, IP="localhost"):
		self.insertOne({"nodeID": nodeID, "numFiles": numFiles, "alive": alive, "IP": IP})


	#increment number of files on a node
	def incFilesOnNode(self, nodeID):
		self.db.incrementOne({"nodeID": nodeID}, {"numFiles": 1})


	#decrement number of files on a node
	def decFilesOnNode(self, nodeID):
		self.db.incrementOne({"nodeID": nodeID}, {"numFiles": -1})