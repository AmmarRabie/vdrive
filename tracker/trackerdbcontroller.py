import sys
sys.path.append('../common')
from dbmanager import DBManager

class TrackerDBController:

	def __init__(self, dbname, host='localhost', port=27017):
		self.db = DBManager(dbname, host, port)


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
		for nodeID in nodesIDs:
				aliveNodes.append(self.db.retrieveOne({"nodeID": nodeID["nodeID"], "alive": True}))
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

	def setNodeBusyState(self, nodeIp, nodePort, isBusy):
		# TODO: implement this function correctly
		desiredNode = self.db.retrieveAllWithAttrWithValue(["nodeID" ,"IP","port","busy"],[None, nodeIp,nodePort,None])
		if (len(desiredNode) == 0):
			print("Cannot Update State error in parameters")
			return False
		
		self.db.updateOne({"nodeID" : int(desiredNode[0]["nodeID"]) ,"port" : nodePort , "IP": nodeIp}, {"busy": isBusy})
		return True

	def updateNodesAliveStates(self, isAliveStates):
		"""
			update the data keepers machines with alive states given

			parameter:
				isAliveStates: a dictionary the key is ip of the machine, value is boolean (true means alive)
		"""
		# TODO: implement this function
		for ip, state in isAliveStates.items():
			# self.db.retrieveAllWithAttrWithValue(["nodeID", "numFiles", "alive", "IP"],[None, None,None,None])
			self.db.updateOne(  {"IP":  ip}, {"alive": state})

		pass

	def getEmptyPortsAllMachines(self):
		"""
			return all free (not busy) not died machines ports for every data keeper machine

			return:
				dict, key is the ip, value is a list of available ports like
				{"192.265.86": ("5560, "786"), "157.264.46.1": ("123",), }
		"""
		# TODO: implement this function
		
		return self.db.retrieveAllWithAttrWithValue(["IP","busy"],[None,False])
		
		pass

	#add file to a node
	def addFileToNode(self, userID, fileName, nodeID):
		self.db.insertOne({"userID":userID ,"fileName": fileName, "nodeID": nodeID})
		self.incFilesOnNode(nodeID)


	#adds a new machine node to the system
	def insertNode(self, nodeID, IP , ports=[6666,6667,6668,6669,6670,6671,6672,6673,6674,6675], numFiles=0, alive=True):
		self.db.insertOne({"nodeID": nodeID, "numFiles": numFiles, "alive": alive,"IP": IP})
		
		for port in ports:
			self.db.insertOne({"nodeID": nodeID, "port":port, "IP": IP , "busy":False})
		


	#increment number of files on a node
	def incFilesOnNode(self, nodeID):
		# self.db.incrementOne({"nodeID": nodeID}, {"numFiles": 1})
		desiredNode = self.db.retrieveAllWithAttrWithValue(["nodeID", "numFiles", "alive", "IP"],[nodeID,None,True,None])
		self.db.incrementOne({ "nodeID": nodeID, "numFiles":int(desiredNode[0]["numFiles"]), "alive":True, "IP": desiredNode[0]["IP"] }, {"numFiles": 1})


	#decrement number of files on a node
	def decFilesOnNode(self, nodeID):
		desiredNode = self.db.retrieveAllWithAttrWithValue(["nodeID", "numFiles", "alive", "IP"],[nodeID,None,True,None])
		self.db.incrementOne({"nodeID": nodeID, "numFiles":int(desiredNode[0]["numFiles"]), "alive":True, "IP":desiredNode[0]["IP"]}, {"numFiles": -1})