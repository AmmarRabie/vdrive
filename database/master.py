'''
paramaters to this script:
every slave ip 
===========================================================================
Master will have 2 threads one for dealing with database and the other one is for keeping track of 
slaves and updating the client with them
============================================================================
Master have 2 connections with client one is REQ/REP for inserting/updating/deleting  and the other one 
is PUB/SUB for updating the client with the status of the slaves
=================================================================================
Master have 2 connections with the slaves the first one is pub-sub connection that will be used to update
their DBs the other one is REP-REQ  which will be only used when a thread that's is not alive returns
back the REP-REQ will be used to update it's database
======================================================================================
toClientSocket =>REQ/REP socket that will  receive from the client when the client wants to insert/delete/retrieve
handleSlavesClientSocket =>PUB/SUB socket that will publish to the clients any change in the slaves
toSlavesSocket => PUB/SUB socket that will publish to the slaves when either a new delete or a new insertion happens
iamAliveSockets => PUB/SUB socket that will be used by the master to ensure that every slave is alive
slaveRecoveryHandlerSocket=>REQ/REP to send the slaves the missed data
'''
import sys  
import zmq
import json
import time
import threading
import pymongo
from aliveSender import *
sys.path.append('../common')
from dbmanager import *
from databaseHandler import *

updateSlavesTopic="55555"
handleSlavesTopic="9999"
iamAliveTopic="12345"


serveUserPort=55555 #this port will be used to handle users requests (retrieve, delete,insert)
updateClientsPort=55556 #this port will be used to update clients with the status of slaves
updateSlavesPort=55557 #this port will be used to update slaves when new insertion or delete happens
iamAliveSocketPort=55558
slaveRecoveryHandlerPort=55559 #this port will be used to update the slave with the missed data

databaseName="usersDatabase"

class Master:
    
    def __init__(self):    
        self.slavesMissedData={}
        self.mydb = DatabaseHandler("usersDatabase")
        self.slavesSockets={}
        #self.slavesIPs=[]
        self.alive={}
        self.context=zmq.Context()
        for i in range (1,len(sys.argv)):
            #toClientiamAliveSockets[i].bind(f"tcp://{SERVER_IP}:{sys.argv[1]}")
            # self.slavesIPs.append(sys.argv[i])
            #self.alive.append(true)
            self.alive[sys.argv[i]]=True
            self.slavesMissedData[sys.argv[i]]=[]
            self.slavesSockets[sys.argv[i]]=(self.context.socket(zmq.REQ))
            self.slavesSockets[sys.argv[i]].bind(f"tcp://{sys.argv[i]}:{updateSlavesPort}")
            self.slavesSockets[sys.argv[i]].setsockopt(zmq.RCVTIMEO, 30)

        self.toClientSocket=self.context.socket(zmq.REP)
        self.toClientSocket.bind(f"tcp://127.0.0.1:{serveUserPort}")
        
        #self.toSlavesSocket=self.context.socket(zmq.PUB)
        #self.toSlavesSocket.bind(f"tcp://127.0.0.1:{updateSlavesPort}")
        self.handleSlavesClientSocket=self.context.socket(zmq.PUB)
        self.handleSlavesClientSocket.bind(f"tcp://127.0.0.1:{updateClientsPort}")

        thread = threading.Thread(target=self.handleSlaves, args=())
        thread.start()
        self.run() 
        
       
          
    def run(self):
        while(True):
            message=self.toClientSocket.recv_json()
            messageDict=json.loads(message)
            if messageDict["operation"]=="insert":
                userDict={
                    "Username":messageDict["Username"],
                    "Password":messageDict["Password"],
                    "Email":messageDict["Email"]
                }

                result=self.mydb.insertUser(userDict)

                if result:
                    #insertion is successful update the slaves
                    toBeSent=updateSlavesTopic+' '+message
                    for key in self.slavesSockets.keys():
                        if self.alive[key]==True:
                            #try to send to the same slave while that slave is alive
                            print (key)
                            print("iteration+++++++++++++++++++++")
                            while True:
                                try:
                                    print ("sending to slave" )
                                    print(self.slavesSockets[key])
                                    print (message)
                                    self.slavesSockets[key].send_json(message)
                                    receivedMessage=self.slavesSockets[key].recv_string()
                                    print (receivedMessage+" from slave")                                    
                                    break
                                except zmq.ZMQError as e :
                                    print("couldn't receive from ")
                                    print(key)
                                    if self.alive[key]==False:
                                        self.slavesMissedData[key].append(message)
                                        break
                    self.toClientSocket.send_string("1") 

                    '''  # self.toSlavesSocket.send_string(toBeSent)
                    #check for any slave that's not alive
                    for key,value in self.alive.items():
                        print (value)
                        if value==False:
                            #print(f"missed data for {key}")
                            self.slavesMissedData[key].append(message)
                    self.toClientSocket.send_string("1") ''' 

                else:
                    self.toClientSocket.send_string("0")

                
                '''
                dictt={
                    "Username":messageDict["Username"]
                }
                #check that the username is never used before
                result=self.mydb.retrieveAll(dictt)
                #print(result+"+++++++++++++++++++++++++++++++++")
                if len(result)==0:
                    userDict={
                        "Password":messageDict["Password"],
                        "Email":messageDict["Email"],
                        "Username":messageDict["Username"]
                    }
                    #insert into my database
                    self.mydb.insertOne(userDict)
                    #send to slaves 
                    print ("done sending")
                    self.toClientSocket.send_string("1")
                   
                    
                else:
                    print("already existed")
                    self.toClientSocket.send_string("0")  
                
                '''      

            elif messageDict["operation"]=="delete":
                #delete from my database
                
                self.mydb.deleteOne({"Username":messageDict["Username"]})
                #send the message to all the alive slaves
                toBeSent=updateSlavesTopic+' '+message
                #self.toSlavesSocket.send_string(toBeSent)
                #store the query for all the dead slaves
                for key,value in self.alive.items():
                    if value==False:
                        self.slavesMissedData[key].append(message)
                self.toClientSocket.send_string("1")        
            elif messageDict["operation"]=="authenticate" :
                result= self.mydb.retrieveOne(messageDict["Username"])  
                self.toClientSocket.send_string(result["Password"])         



                            
    def handleSlaves(self):
        iamAliveSocket=self.context.socket(zmq.SUB)
        iamAliveSocket.setsockopt_string(zmq.SUBSCRIBE, iamAliveTopic)
        for key in self.alive.keys():
            print(key)
            iamAliveSocket.connect(f"tcp://127.0.0.1:{iamAliveSocketPort}")
            print ("connected!")
        
        
        iamAliveSocket.setsockopt(zmq.RCVTIMEO, 30)
        while(True):
            #try to receive from every slave im alive signal
            currentAliveSlaves=[]
            currentTime=time.time()
            endTime=currentTime+1
            while time.time()<endTime:
                try:    
                    #print("trying to receive from any slave")
                    message=iamAliveSocket.recv_string()
                    topic,ip=message.split()
                    currentAliveSlaves.append(ip)
                except zmq.ZMQError as e :
                    pass    
           # print ("done one loop")        
            for key in self.alive.keys():
                if key in currentAliveSlaves:
                    if self.alive[key]==False:
                        #print(f"the slave with ip {key} is dead")
                        self.alive[key]=True
                        thread = threading.Thread(target=self.slaveRecoveryHandler, args=(key,))
                        thread.start()

                else:
                    #pass
                  #  print (key,)
                    self.alive[key]=False
                    thread = threading.Thread(target=self.disconnectSlave, args=(key,))
                    thread.start()
            
            
            '''
            
            for i in range len(slavesIPs):
                try:
                    message=iamAliveSockets[i].recv_json()
                    if(alive[message["address"]]==False):
                        thread = threading.Thread(target=self.slaveRecoveryHandler, args=(message["address"]))
                        thread.start()
                    
                        #send the missed data to the slave and receive an ack from it
                        
                        iamAliveSockets[i].send_json(json.dumps(slavesMissedData[i]))
                        #receive an ack from the slave
                        iamAliveSockets[i].recv()
                        #send to the client to connect to this slave again
                        

                except zmq.ZMQError as e:
                    if e.errno == zmq.EAGAIN and alive[i]==true:
                        alive[i]=false
                        #send the slave IP  to the client to remove this ip
                        messageDict={
                            "command":"disconnect",
                            "address":slavesIPs[i]
                        }
                        handleSlavesClientSocket.send_json(handleSlavesTopic,json.dumps(messageDict))
                        '''
    def slaveRecoveryHandler(self,address):
        slaveRecoveryHandlerSocket=self.context.socket(zmq.REQ)
        slaveRecoveryHandlerSocket.connect(f"tcp://{address}:{slaveRecoveryHandlerPort}")
        slaveRecoveryHandlerSocket.send_json(self.slavesMissedData[address])
        print(f"sending to slave{self.slavesMissedData[address]}")
        message=slaveRecoveryHandlerSocket.recv()
        if message=="1":
            #successsfully updated the slave,send to all clients that the slave is alive now
            messageDict={
                            "command":"connect",
                            "address":address
                        }
            self.handleSlavesClientSocket.send_json(handleSlavesTopic,json.dumps(messageDict))
            self.alive[address]=True
        slaveRecoveryHandlerSocket.close()    


    def disconnectSlave(self,address):
        messageDict={
            "command":"disconnect",
            "address":address[0]
        }
        toBeSent=handleSlavesTopic+' '+json.dumps(messageDict)
        self.handleSlavesClientSocket.send_string(toBeSent)
#time.sleep(10)
m=Master()        