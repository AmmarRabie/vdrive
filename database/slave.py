'''
Paramters to this script:Master ip 
==========================================
slave has 3 connections with master:
1-PUB/SUB connection for updating the slave's database
2-PUB/SUB connection for implementing the iamAlive 
3-REQ/REP connection for sending the missed data if the slave went down
====================================================
slave has 1 connection with the client:
1-REQ/REP connection for retrieeving user data
'''
import sys  
import zmq
import json
import time
import threading
import pymongo
from ast import literal_eval
from aliveSender import *
sys.path.append('../common')
from dbmanager import *

updateSlavesTopic="55555"
handleSlavesTopic="9999"
iamAliveTopic="12345"


serveUserPort=5555 #this port will be used to handle users requests (retrieve, delete,insert)
updateClientsPort=55556 #this port will be used to update clients with the status of slaves
updateSlavesPort=55557 #this port will be used to update slaves when new insertion or delete happens
iamAliveSocketPort=55558
slaveRecoveryHandlerPort=55559 #this port will be used to update the slave with the missed data


class Slave:
    def __init__ (self):
        self.mydb = DBManager("usersDatabaseSlave1")
        self.context=zmq.Context()
        
        self.toClientSocket=self.context.socket(zmq.REP)
        self.toClientSocket.bind(f"tcp://127.0.0.1:{serveUserPort}")
        
        self.toMasterSocket=self.context.socket(zmq.SUB)
        self.toMasterSocket.connect(f"tcp://{sys.argv[1]}:{updateSlavesPort}")
        self.toMasterSocket.setsockopt_string(zmq.SUBSCRIBE, updateSlavesTopic)
        #self.toMasterSocket.setsockopt(zmq.RCVTIMEO, 30)
        
        self.iamAliveSocket=self.context.socket(zmq.PUB)
        self.iamAliveSocket.bind(f"tcp://127.0.0.1:{iamAliveSocketPort}")

        self.recoveryHandlerSocket=self.context.socket(zmq.REP)
        self.recoveryHandlerSocket.bind(f"tcp://127.0.0.1:{slaveRecoveryHandlerPort}")


        iamAliveThread=threading.Thread(target=self.sendIamAlive,args=())
        updateDBThread=threading.Thread(target=self.updateDB,args=())
        recoveryHandlerThread=threading.Thread(target=self.recoverSlave,args=())

        iamAliveThread.start()
        updateDBThread.start()
        recoveryHandlerThread.start()

        self.run()
    def run(self):
        #this method will run in the main thread it will be responsible for receiving requests from the user
        while True:
            message=self.toClientSocket.recv_json()
            print ("receivedddddddddddddddddddddddddddddddd")
            messageDict=json.loads(message)
            toDbDict={
                "Username":messageDict["Username"]
            }    
            result=self.mydb.retrieveOne(toDbDict)

            print(result)
            toBeSent={
                "Password":result["Password"]
            }
            self.toClientSocket.send_json(json.dumps(toBeSent))

    def sendIamAlive(self):
        while True:
            #print ("sending my ip")
            toBeSent=iamAliveTopic+' '+"127.0.0.1"
            #print (toBeSent)
            self.iamAliveSocket.send_string(toBeSent)
            #print("sent")
            #time.sleep(5)
    def updateDB(self):
        while True:
            message=self.toMasterSocket.recv_string()
            print (message[1])
            topic,messageString=message.split("{")
            messageString="{"+messageString
            messageDict=literal_eval(messageString)
            #messageDict=json.loads(message)
            if messageDict["operation"]=="insert":

                toBeAdded={
                    "Username":messageDict["Username"],
                    "Password":messageDict["Password"],
                    "Email":messageDict["Email"]
                }
                self.mydb.insertOne(toBeAdded)
            else:
                toBeDeleted={
                    "Username":messageDict["Username"]
                }    
                self.mydb.deleteOne(toBeDeleted)
    def recoverSlave(self):
        while True:
            message=self.recoveryHandlerSocket.recv_json()
            #insert the missed data
            print (message)
            #send ack to master
            self.recoveryHandlerSocket.send_string("1")




#time.sleep(10)
s=Slave()


