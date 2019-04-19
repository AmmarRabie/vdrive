import sys
sys.path.append('../common')
from dbmanager import DBManager


class TrackerDBController:

	def __init__(self, dbname, host='localhost', port='27017'):
		self.db = DBManager(dbname)


	#used for ls command
	def getUserFiles(self, userID):
		# files = self.db.retrieveAll({"userID": userID})
		# fileNames = []
		# for item in files:
		# 	fileNames.append(files["fileName"])
		# return fileNames
		queryOutput =  self.db.retrieveAllWithAttrWithValue(["userID","fileName"],[userID,None])

		objects = []

		for value in queryOutput:
			if value["fileName"] not in objects:
				objects.append(value["fileName"])

		return objects


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


	# Retrieves all records having these attributes 
	# for each attribute pass value
	# if value does not matter just pass None
	# Example ["nodeID","fileName"],[None,"1.mp4"]
	def retrAllHaveAttrWithValue(self,attributes,values):
		return self.db.retrieveAllWithAttrWithValue(attributes,values)

	# Returns list of all files' name
	def listAllFilesAllUsers(self):
		queryOutput =  self.db.retrieveAllWithAttrWithValue(["userID","fileName"],[None,None])

		objects = []

		for value in queryOutput:
			if value not in objects:
				objects.append(value)

		return objects

	# Returns list of all Nodes' ids
	def listAllNodes(self):
		queryOutput =  self.db.retrieveAllWithAttrWithValue(["nodeID", "numFiles", "alive", "IP"],[None,None,None,None,None])

		# objects = []

		# for value in queryOutput:
		# 	if value["nodeID"] not in objects:
		# 		objects.append(value["nodeID"])

		# return objects
		return queryOutput

	def getInstancesOfFile(self,userID,fileName):
		queryOutput =  self.db.retrieveAllWithAttrWithValue(["userID","fileName"],[userID,fileName])
		return len(queryOutput)

	# Returns list of all Nodes' ids

	def listAliveNodes(self):
		queryOutput =  self.db.retrieveAllWithAttrWithValue(["nodeID", "numFiles", "alive", "IP"],[None,None,True,None])

		# objects = []

		# for value in queryOutput:
		# 	if value["nodeID"] not in objects:
		# 		objects.append(value["nodeID"])

		# return objects
		return queryOutput
	

	#insert a new file for a specefic user in node
	def insertFile(self, userID, fileName, nodeID):
		self.db.insertOne({"userID": userID, "fileName": fileName , "nodeID":nodeID})
		desiredNode = self.db.retrieveAllWithAttrWithValue(["nodeID", "numFiles", "alive", "IP"],[nodeID,None,True,None])
		self.db.incrementOne({ "nodeID": nodeID, "numFiles":int(desiredNode[0]["numFiles"]), "alive":True, "IP": desiredNode[0]["IP"] }, {"numFiles": 1})



	#make the node alive or not
	#alive is a bool variable
	def setNodeState(self, nodeID, alive):
		self.db.updateOne({"nodeID": nodeID}, {"alive": alive})


	#add file to a node
	def addFileToNode(self, userID, fileName, nodeID):
		self.db.insertOne({"userID":userID ,"fileName": fileName, "nodeID": nodeID})
		self.incFilesOnNode(nodeID)


	#adds a new machine node to the system
	def insertNode(self, nodeID, numFiles=0, alive=True, IP="localhost"):
		self.db.insertOne({"nodeID": nodeID, "numFiles": numFiles, "alive": alive, "IP": IP})


	#increment number of files on a node
	def incFilesOnNode(self, nodeID):
		# self.db.incrementOne({"nodeID": nodeID}, {"numFiles": 1})
		desiredNode = self.db.retrieveAllWithAttrWithValue(["nodeID", "numFiles", "alive", "IP"],[nodeID,None,True,None])
		self.db.incrementOne({ "nodeID": nodeID, "numFiles":int(desiredNode[0]["numFiles"]), "alive":True, "IP": desiredNode[0]["IP"] }, {"numFiles": 1})


	#decrement number of files on a node
	def decFilesOnNode(self, nodeID):
		desiredNode = self.db.retrieveAllWithAttrWithValue(["nodeID", "numFiles", "alive", "IP"],[nodeID,None,True,None])
		self.db.incrementOne({"nodeID": nodeID, "numFiles":int(desiredNode[0]["numFiles"]), "alive":True, "IP":desiredNode[0]["IP"]}, {"numFiles": -1})