import pymongo


class DBManager:

	def __init__(self, dbname, host="localhost", port=27017):
		self.client = pymongo.MongoClient(host, port)
		self.db = self.client.get_database(dbname)


	#dictToInsert will be like
	# {"x": 10, "y":20, "z": 30}
	def insertOne(self, dictToInsert):
		return self.db.my_collection.insert_one(dictToInsert)


	#key will be like
	# {"key": value}
	def retrieveOne(self, key):
		return self.db.my_collection.find_one(key)


	#key will be like
	# {"key": value}
	# returns a list of dictionaries
	def retrieveAll(self, key):
		objects = []
		for item in self.db.my_collection.find(key):
			objects.append(item)
		return objects

	# # returns all records having thess attributes
	# def retrieveAllWithAttr(self,attributes):
	# 	# return self.db.my_collection.count({})
	# 	dictionary = {}
	# 	for attribute in attributes:
	# 		dictionary[attribute] = {'$exists': True}
	# 	return self.db.my_collection.find(dictionary)

	def retrieveAllWithAttrWithValue(self,attributes,values):
		dictionary = {}
		dictionary2 = {}
		i = 0
		for attribute in attributes:
			dictionary[attribute] = {'$exists': True}
			if (values[i] != None):
				dictionary2[attribute] = values[i]
			i+=1

		queryOutput = self.db.my_collection.find({"$and": [dictionary, dictionary2] },{'_id': False})

		objects = []
		for data in queryOutput:
			objects.append(data)
			
		return objects


	#key will be like
	# {"key": value}
	def deleteOne(self, key):
		self.db.my_collection.delete_one(key)


	#key and update will be like
	# {"key": value}
	def updateOne(self, key, update):
		self.db.my_collection.update_one(key, { '$set':update}, upsert=True).raw_result

	def findAndUpdate(self, key, update):
		return self.db.my_collection.find_one_and_update(key, { '$set':update}, upsert=True)


	#increments a value with a specefic number
	# if update = {"x": 3}
	# then x will be incremented by 2
	def incrementOne(self, key, update):
		self.db.my_collection.update_one(key, { '$inc':update}, upsert=True)
	




if __name__ == "__main__":
	# dbmanager = DBManager("Wagih")
	# dbmanager.insertOne({"name": "omar", "email": "omarsgalal4@gmail.com"})
	# print(dbmanager.retrieveOne({"name":"omar"}))
	# dbmanager.updateOne({"name":"omar"}, {'email':'omar'})
	# print(dbmanager.retrieveOne({"name":"omar"}))
	# dbmanager.deleteOne({"name":"omar"})
	# print(dbmanager.retrieveOne({"name":"omar"}))
	x = 1