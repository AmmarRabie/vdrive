import sys
sys.path.append('../common')
from dbmanager import DBManager

class TrackerDBController:

	def __init__(self, dbname, host='localhost', port=27017):
		self.db = DBManager(dbname, host, port)


	#used for ls command
	# returns list of file names [ "1.mp4", "2.mp4" ]
	def getUserFiles(self, userID):
		queryOutput =  self.db.retrieveAllWithAttrWithValue(["userID","fileName"],[userID,None])

		objects = []

		for value in queryOutput:
			if value["fileName"] not in objects:
				objects.append(value["fileName"])

		return objects


	#returns True if node is alive and False if not
	def isNodeAlive(self, nodeIp):
		return self.db.retrieveOne({"nodeIP": nodeIp})["alive"]


	#return the number of files on the node
	def getNodeNumberOfFiles(self, nodeIp):
		return self.db.retrieveOne({"nodeIP": nodeIp})["numFiles"]


	#returns alive nodes IDs where the file is there
	def getFileNodes(self, fileName):
		records = self.db.retrieveAll({"fileName": fileName})
		aliveNodes = []
		for record in records:
				aliveNodes.append(self.db.retrieveOne({"nodeIP": record["nodeIP"], "alive": True}))
		return aliveNodes

	# Function takes file info and gets list of nodes' ip that holds this file
	# returns list of node's ip [100,200,300]
	def getNodesOfFile(self,userID,fileName):
		#gets list of all nodes have this file userID, fileName, nodeIP
		quereyOutput = self.retrAllHaveAttrWithValue(["userID","fileName"],[userID,fileName])
		nodeIPs = []
		for record in quereyOutput:
			nodeIPs.append(record["nodeIP"])

		return nodeIPs

	# Function takes file info and prepare it for download
	# gets list of all machine ips and its free ports
	# returns [ [nodeIP, [port1,port2]  ] ]
	def getPortsForDownload(self,userID,fileName):

		nodeIPs = self.getNodesOfFile(userID,fileName)

		#gets list of all empty ports on all machines 
		emptyPortsOfAll = self.getEmptyPortsAllMachines()

		# print(emptyPortsOfAll)

		output = []

		i = 0

		while i < len(emptyPortsOfAll):
			ports = []
			currentIP = emptyPortsOfAll[i]["nodeIP"]

			while emptyPortsOfAll[i]["nodeIP"] in nodeIPs and emptyPortsOfAll[i]["nodeIP"] == currentIP:
				ports.append(emptyPortsOfAll[i]["port"])
				i += 1
				if(i == len(emptyPortsOfAll)):
					break
				
			
			if len(ports) == 0:
				i += 1
			else:
				output.append([currentIP,ports])
				
		return output
		

	# Retrieves all records having these attributes 
	# for each attribute pass value
	# if value does not matter just pass None
	# Example ["nodeID","fileName"],[None,"1.mp4"]
	def retrAllHaveAttrWithValue(self,attributes,values):
		return self.db.retrieveAllWithAttrWithValue(attributes,values)

	# Returns list of all files' name
	def listAllFilesAllUsers(self):
		queryOutput =  self.retrAllHaveAttrWithValue(["userID","fileName"],[None,None])

		objects = []

		for value in queryOutput:
			if value not in objects:
				objects.append(value)

		return objects

	# Returns list of all Nodes' ids
	def listAllNodes(self):
		queryOutput =  self.retrAllHaveAttrWithValue(["nodeIP", "numFiles", "alive"],[None,None,None])
		
		return queryOutput

	# Get number of instances of specific files
	# returns 3 ==> this file exists on 3 machines
	def getInstancesOfFile(self,userID,fileName):
		queryOutput =  self.retrAllHaveAttrWithValue(["userID","fileName"],[userID,fileName])
		return len(queryOutput)

	# Returns list of all alive Nodes
	def listAliveNodes(self):
		queryOutput =  self.retrAllHaveAttrWithValue(["nodeIP", "numFiles", "alive"],[None,None,True])

		return queryOutput
	

	#insert a new file for a specefic user in node
	def insertFile(self, userID, fileName, nodeIp):
		#insert file
		self.db.insertOne({"userID": userID, "fileName": fileName , "nodeIP":nodeIp})
		#get node that file is inserted to
		desiredNode = self.retrAllHaveAttrWithValue(["nodeIP", "numFiles", "alive"],[nodeIp,None,True])
		print(desiredNode, userID, fileName, nodeIp)
		#increment number of files this node has
		self.db.incrementOne({ "nodeIP": desiredNode[0]["nodeIP"], "numFiles":int(desiredNode[0]["numFiles"]), "alive":True }, {"numFiles": 1})



	#make the node alive or not
	#alive is a bool variable
	def setNodeState(self, nodeIp, alive):
		self.db.updateOne({"nodeIP": nodeIp}, {"alive": alive})


	def setNodeBusyState(self, nodeIp, nodePort, isBusy):
		# TODO: implement this function correctly
		desiredNode = self.retrAllHaveAttrWithValue(["nodeIP","port","busy"],[ nodeIp,nodePort,None])
		
		if (len(desiredNode) == 0):
			print("Cannot Update State error in parameters")
			return False
		
		# self.db.updateOne({"nodeIP" : int(desiredNode[0]["nodeIP"]) ,"port" : nodePort}, {"busy": isBusy})
		self.db.updateOne({"nodeIP" : desiredNode[0]["nodeIP"] ,"port" : nodePort}, {"busy": isBusy})
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
			self.db.updateOne(  {"nodeIP":  ip, "port": "-1"}, {"alive": state})

		pass

	def getEmptyPortsAllMachines(self):
		"""
			return all free (not busy) not died machines ports for every data keeper machine

			return:
				dict, key is the ip, value is a list of available ports like
				{"192.265.86": ("5560, "786"), "157.264.46.1": ("123",), }
		"""
		# TODO: implement this function
		
		return self.retrAllHaveAttrWithValue(["nodeIP","busy"],[None,False])

	#add file to a node
	def addFileToNode(self, userID, fileName, nodeIp):
		self.db.insertOne({"userID":userID ,"fileName": fileName, "nodeIP": nodeIp})
		self.incFilesOnNode(nodeIp)


	#adds a new machine node to the system
	def insertNode(self, nodeIp, ports=[6666,6667,6668,6669,6670,6671,6672,6673,6674,6675], numFiles=0, alive=True):
		self.db.insertOne({"nodeIP": nodeIp,"port": "-1", "numFiles": numFiles, "alive": alive})
		
		for port in ports:
			self.db.insertOne({"nodeIP": nodeIp, "port":port , "busy":False})
		


	#increment number of files on a node
	def incFilesOnNode(self, nodeIp):
		# self.db.incrementOne({"nodeID": nodeID}, {"numFiles": 1})
		desiredNode = self.retrAllHaveAttrWithValue(["nodeIP", "numFiles", "alive"],[nodeIp,None,True])
		self.db.incrementOne({ "nodeIP": nodeIp, "numFiles":int(desiredNode[0]["numFiles"]), "alive":True }, {"numFiles": 1})


	#decrement number of files on a node
	def decFilesOnNode(self, nodeIp):
		desiredNode = self.retrAllHaveAttrWithValue(["nodeIP", "numFiles", "alive", "IP"],[nodeIp,None,True,None])
		self.db.incrementOne({"nodeIP": nodeIp, "numFiles":int(desiredNode[0]["numFiles"]), "alive":True}, {"numFiles": -1})


if __name__ == "__main__":
	cont = TrackerDBController("TrackerDB")
	# cont.insertNode("192.168.1.2")
	# cont.insertNode("192.168.1.3")
	# cont.insertNode("192.168.1.4")
	# cont.addFileToNode(1, "1.mp4", "192.168.1.2")
	# cont.addFileToNode(1, "1.mp4", "192.168.1.3")
	# cont.addFileToNode(1, "1.mp4", "192.168.1.4")
	print(cont.getPortsForDownload(1, "1.mp4"))