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
sys.path.append('../')
from common.util import *
from common.dbmanager import *
from databaseHandler import *
from appconfig import serveUserPort, updateClientsPort, updateSlavesPort, iamAliveSocketPort, slaveRecoveryHandlerPort

updateSlavesTopic="55555"
handleSlavesTopic="9999"
iamAliveTopic="12345"


class Slave:
    def __init__ (self):
        self.mydb = DatabaseHandler("usersDatabaseSlave1")
        self.context=zmq.Context()
        
        self.toClientSocket=self.context.socket(zmq.REP)
        self.toClientSocket.bind(f"tcp://*:{serveUserPort-1}")
        
        self.toMasterSocket=self.context.socket(zmq.REP)
        self.toMasterSocket.bind(f"tcp://*:{updateSlavesPort}")
        #self.toMasterSocket.setsockopt_string(zmq.SUBSCRIBE, updateSlavesTopic)
        #self.toMasterSocket.setsockopt(zmq.RCVTIMEO, 30)
        
        self.iamAliveSocket=self.context.socket(zmq.PUB)
        self.iamAliveSocket.bind(f"tcp://*:{iamAliveSocketPort}")

        self.recoveryHandlerSocket=self.context.socket(zmq.REP)
        self.recoveryHandlerSocket.bind(f"tcp://*:{slaveRecoveryHandlerPort}")


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
            print ("[run] received from client",message)
            messageDict=json.loads(message)
            User=self.mydb.retrieveUser({"Username":messageDict["Username"]})
            if User["Password"]==messageDict["Password"]:
                self.toClientSocket.send_string("1")
            else:
                self.toClientSocket.send_string("0")    

            
    def sendIamAlive(self):
        while True:
            #print ("sending my ip")
            toBeSent=iamAliveTopic+' '+getCurrMachineIp()
            #print (toBeSent)
            self.iamAliveSocket.send_string(toBeSent)
            #print("sent")
            #time.sleep(5)
    def updateDB(self):
        while True:
            message=self.toMasterSocket.recv_json()
            print("[UpdateDB] received from master ",message)
            messageDict=json.loads(message)
            if messageDict["operation"]=="insert":

                toBeAdded={
                    "Username":messageDict["Username"],
                    "Password":messageDict["Password"],
                    "Email":messageDict["Email"]
                }
                self.mydb.insertUser(toBeAdded)
            else:
                toBeDeleted={
                    "Username":messageDict["Username"]
                }    
                self.mydb.deleteUser(toBeDeleted)
            self.toMasterSocket.send_string("1")    
    def recoverSlave(self):
        while True:
            message=self.recoveryHandlerSocket.recv_json()
            #insert the missed data
            print ("recovering the db ",message)
            ''' for stringOperation in message:
                operationDict=literal_eval(stringOperation)
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
                    self.mydb.deleteOne(toBeDeleted)
            '''
            self.mydb.recoverDB(message)    
            #send ack to master
            self.recoveryHandlerSocket.send_string("1")




#time.sleep(10)
s=Slave()


