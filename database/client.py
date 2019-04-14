'''
paramaters to this script:
1-master ip followed by the port number that will be used to handle slaves
2-master ip followed by the port number for reading/inserting/deleting from DB
2-slaves ip with the port number for every slave
=================================================
Client contains 2 threads one for inserting/deleting/Authenticating users
the other one is for connecting or disconnecting with the slaves
'''

import zmq
import json
import threading
class Client:
    def __init__(self):
        """"
        at init establish the connection with the master and slaves script
        """
        context = zmq.Context()
        insertSocket=context.socket(zmq.REQ)
        inserSocket.connect(f"tcp://{sys.argv[2]}")
        readSocket = context.socket(zmq.REQ)
        for i in range (2,len (sys.argv)):            
            readSocket.connect(f"tcp://{sys.argv[i]}")
        thread = threading.Thread(target=self.handleSlaves, args=(context,readSocket))    


    def register(self,username,password,email):
        
        #todo check that data is valid
        dictMessage={
            "Username":username,
            "password":password,
            "email":email,
            "operation":"insert"
        }       
        insertSocket.send_json(json.dumps(dictMessage))
        
        message=inserSocket.recv()
        
        #if received message =1 insertion is succesfull else unsuccessful
        
        return message

    def delete(self,username):
        #Assume that the user already signed in
        dictMessage={
            "Username":username,
            "operation":"delete"
        }
        inserSocket.send_json(json.dumps(dictMessage))
        message=inserSocket.recv()
        #if 1 successfull delete 
        return message
    def Authenticate(self,username,password):
        
        dictMessage={
            "Username":username,
            "operation":"authenticate"
        }
        readSocket.send_json(json.dumps(dictMessage))
        #message will contain the password 
        message=readSocket.recv()
        if message == password:
            return "1"
        return "0"
    def handleSlaves(self,context,readSocket):
        handleSlavesSocket=context.socket(zmq.REQ)
        handleSlavesSocket.connect(f"tcp:\\{sys.argv[1]}")
        while true:
            message=socket.recv_json()
            dictMessage=json.loads(message)
            if dictMessage["command"]=="disconnect":
                zmq_disconnect(readSocket,dictMessage["address"])
            if dictMessage["command"]== "connect":
                zmq_connect(readSocket,dictMessage["address"])    



    



