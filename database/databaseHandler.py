import sys  
from ast import literal_eval
sys.path.append('../common')
from dbmanager import *

class DatabaseHandler:
    def __init__(self,dbname):
        self.mydb=DBManager(dbname)
    def insertUser(self,UserDict):
        #check that the username is not taken
        usernameDict={
            "Username":UserDict["Username"]
        }    
        result=self.mydb.retrieveAll(usernameDict)
        if len(result)==0:
            self.mydb.insertOne(UserDict)
            return True
        else:
            return False
    def retrieveUser(self,usernameDict):
        user=self.mydb.retrieveOne({"Username":usernameDict})
        return user
    def deleteUser(self,usernameDict):
        print("database/databaseHandler in deleteUser", usernameDict)
        self.mydb.deleteOne({"Username": usernameDict})
    def recoverDB(self,operationsArray):
        for stringOperation in operationsArray:
                
                operationDict=literal_eval(stringOperation)
                print(operationDict,"dict while recovering db")
                if(operationDict["operation"]=="insert"):
                    toBeInserted={
                        "Username":operationDict["Username"],
                        "Password":operationDict["Password"],
                        "Email":operationDict["Email"]
                    }
                    self.mydb.insertOne(toBeInserted)
                else:
                    toBeDeleted={
                        "Username":operationDict["Username"]
                    }
                    self.deleteOne(toBeDeleted)
        


        
            

