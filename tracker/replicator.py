import time
from trackerdbcontroller import TrackerDBController

class Replicator:

    dbManager = None

    maximumFilesOnNode = 0

    filesLocations = []

    nodesStates = {}


    def __init__(self, dbname="TrackerDB"):

        self.db = TrackerDBController(dbname)

        # self.db.insertNode(100,"192.168.1.1")
        # self.db.insertNode(110,"192.168.1.2")
        # self.db.insertNode(120,"192.168.1.3")

        # self.db.insertFile("mai","1.mp4",100)
        # self.db.insertFile("mai","2.mp4",100)
        # self.db.insertFile("aya","5.mp4",100)
        # self.db.insertFile("aya","6.mp4",100)
        # self.db.insertFile("mai","6.mp4",100)

# ######################################################################


    def replicator_process(self):
        
        # filesLocations = self.db.retrAllHaveAttrWithValue(["nodeID","fileName"],[None,None])

        ################################ Gets list of files but assume no 2 users have the same filename
        listOfFiles = self.db.listAllFilesAllUsers()

        listOfNodes = self.db.listAliveNodes()
        print()
        
        # print("filesLocations = ",filesLocations)
        # print()

        print("listOfFiles",listOfFiles)
        print()

        # print("listOfNodes = ",listOfNodes)
        # print()
    
        listOfNodes = sorted(listOfNodes, key=lambda k: k["numFiles"]) #, reverse=True) 
        
        print("listOfNodes = ",listOfNodes)
        print()


        
        for file in listOfFiles:
            # print (file)

            # instances = (sum(value["fileName"] == file["fileName"] for value in filesLocations))
            instances = self.db.getInstancesOfFile(file["userID"],file["fileName"])

            src = next(item for item in listOfNodes if item["nodeID"] == file["nodeID"])
            # src = next((item for item in listOfNodes if item["nodeID"] == "Pam"), None)

            print("src = ", src)

            # print(instances)
            if (instances == 1):
                x = 1

                dest1 = next(item for item in listOfNodes if ( item != src ))

                dest2 = next(item for item in listOfNodes if ( item != src and item != dest1 ))
                
                print("dest1 = ",dest1," dest2 = ",dest2)
                ############################ Call function to upload to dest1

                ############################ Call function to upload to dest2

            elif (instances == 2):

                dest1 = next(item for item in listOfNodes if ( item != src))

                print("dest1 = ",dest1)

                ############################ Call function to upload to dest1


                


if __name__ == '__main__':
    replicatorObject = Replicator("TrackerDB")


    while(True):
        # replicatorObject.replicator_process()
        time.sleep(5)