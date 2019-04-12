import pymongo


class DBManager:

	def __init__(self, dbname, host="localhost", port=27017):
		self.client = pymongo.MongoClient(host, port)
		self.db = self.client.get_database(dbname)


	#dictToInsert will be like
	# {"x": 10, "y":20, "z": 30}
	def insertOne(self, dictToInsert):
		self.db.my_collection.insert_one(dictToInsert)


	#key will be like
	# {"key": value}
	def retrieveOne(self, key):
		return self.db.my_collection.find_one(key)

	#key will be like
	# {"key": value}
	def deleteOne(self, key):
		self.db.my_collection.delete_one(key)


if __name__ == "__main__":
	dbmanager = DBManager("Wagih")
	dbmanager.insertOne({"name": "omar", "email": "omarsgalal4@gmail.com"})
	print(dbmanager.retrieveOne({"name":"omar"}))
	dbmanager.deleteOne({"name":"omar"})
	print(dbmanager.retrieveOne({"name":"omar"}))