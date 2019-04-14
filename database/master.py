'''
paramaters to this script:
1-the client ip with the port that will be used to handle slaves
2-the client ip with the port that will be used for dealing with DB
3-every slave with it's ip address and  port
===========================================================================
Master will have 2 threads one for dealing with database and the other one is for keeping track of 
slaves and updating the client with them
============================================================================
Master have 2 connections with client one for inserting/updating/deleting and the other one for
updating the client with the status of the slaves
=================================================================================
Master have 2 connections with the slaves the first one is pub-sub connection that will be used to update
their DBs the other one is REP-REQ  which will be only used when a thread that's is not alive returns
back the REP-REQ will be used to update it's database
'''

import zmq
import json
import threading
import pymongo
from aliveSender import *
from dbmanager import *

insertTopic=55555
class Master:
    
    def __init__(self):    
        slavesIPs[]
        alive[]
        try:
            context=zmq.context()
            for i in range (3,len(sys.argv[])):
                #toClientSockets[i].bind(f"tcp://{SERVER_IP}:{sys.argv[1]}")
                slavesIPs[i]=sys.argv[i]
                alive[i]=true

            toClientSocket=context.socket(zmq.REP)
            toClientSocket.bind(f"tcp://{SERVER_IP}:{sys.argv[1]}")
            toSlavesSocket=context.socket(zmq.PUB)
            toSlavesSocket.bind(f"tcp://{SERVER_IP}:{sys.argv[2]}")
            thread = threading.Thread(target=self.handleSlaves, args=(context,slaves,alive))

            #connect to database            
            mydb = DBManager("MyDataBase")
        except Error as e:
            print(e)
        run()    
    def run(self):
        while(true):
            message=toClientSocket.recv_json()
            messageDict=json.loads(message)
            if messageDict["operation"]=="insert":
                try:
                    cur.execute(messageDict["query"],messageDict["values"])
                    db.commit()
                    #publish to the slaves
                    toSlavesSocket.send_json(insertTopic,message)


                except mysql.connector.Error as error:
                    db.rollback()
            else:
                #retrive            
    def handleSlaves(self,context,slavesIPs,alive):
        sockets=[]
        #open connection with the client at the port that's responsible connecting/disconnecting slaves
        handleSlavesClientSocket=context.socket(zmq.REP)
        handleSlavesClientSocket.bind(f"tcp\\{sys.argv[1]}")
        #open connection with every slave and set the blocking time of receive
        for i in range len(slavesIPs):
            sockets[i]=context.socket(zmq.REQ)
            sockets[i].bind(f"tcp:\\{slavesIPs[i]}")
            sockets[i].setsockopt(zmq.RCVTIMEO, 30)
        while(true):
            #try to receive from every slave im alive signal
            for i in range len(slavesIPs):
                try:
                    sockets[i].recv()
                    if(alive[i]==false):
                        #send the missed data to the slave and receive an ack from it
                        

                        #send to the client to connect to this slave again
                except zmq.ZMQError as e:
                    if e.errno == zmq.EAGAIN and alive[i]==true:
                        alive[i]=false
                        #send the slave IP  to the client to remove this ip
                        messageDict={
                            "command":"disconnect",
                            "address":slavesIPs[i]
                        }
                        handleSlavesClientSocket.send_json(json.dumps(messageDict))







                
            

