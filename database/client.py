'''
paramaters to this script:
1-master ip followed by the port number that will be used to handle slaves
2-master ip followed by the port number for reading/inserting/deleting from DB
2-slaves ip with the port number for every slave
=================================================
Client contains 2 threads one for inserting/deleting/Authenticating users
the other one is for connecting or disconnecting with the slaves
'''

import sys
sys.path.append("../")
import zmq
import json
import threading
from ast import literal_eval
from common.util import generateToken
from common.util import getCurrMachineIp
handleSlavesTopic="9999"
from appconfig import serveUserPort, updateClientsPort, updateSlavesPort, iamAliveSocketPort, slaveRecoveryHandlerPort,SLAVES_IPS,MASTER_IP

class Client:
    def __init__(self):
        #at init establish the connection with the master and slaves script
        self.context = zmq.Context()
        self.insertSocket=self.context.socket(zmq.REQ)
        self.insertSocket.connect(f"tcp://{MASTER_IP}:{serveUserPort}")
        print(getCurrMachineIp())
        print("+++++++++++++++++++++++++++++")
        self.readSocket =self.context.socket(zmq.REQ)
        self.readSocket.setsockopt(zmq.RCVTIMEO, 500)   
        self.readSocket.connect(f"tcp://{MASTER_IP}:{serveUserPort}")
        for ip in SLAVES_IPS :            
            self.readSocket.connect(f"tcp://{ip}:{serveUserPort}")
        thread = threading.Thread(target=self.handleSlaves, args=())
        thread.start()    


    def register(self,username,password,email):
        
        #todo check that data is valid
        dictMessage={
            "Username":username,
            "Password":password,
            "Email":email,
            "operation":"insert"
        }
        print("sending to master with ip")
        #   print(sys.argv[1])
        print(serveUserPort)       
        self.insertSocket.send_json(json.dumps(dictMessage))
        print("sent")
        try:
            message=self.insertSocket.recv_string()
            print ("received from master")
            print(message)
            token = generateToken(username, password) if message == "1" else ""
            return token
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                #Master is dead!
                return -1


        

    def delete(self,token):
        #Assume that the user already signed in
        dictMessage={
            "token":token,
            "operation":"delete"
        }
        self.insertSocket.send_json(json.dumps(dictMessage))
        try:
            message=self.insertSocket.recv_string()
            return message
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                #Master is dead!
                return -1


    def authenticate(self,username,password):
        dictMessage={
            "Username":username,
            "Password":password,
            "operation":"authenticate"
        }
        print("database/client: authenticate function dict", dictMessage)
        self.readSocket.send_json(json.dumps(dictMessage))
        while True:
            try:
                message=self.readSocket.recv_string()
                print("message")
                if message == "1":
                    return generateToken(username, password)
                return ""
            except zmq.ZMQError as e:
                print("couldn't receive")
                pass
                #do nothing the client will  try to send to another DB

    def handleSlaves(self):
        handleSlavesSocket=self.context.socket(zmq.SUB)
        handleSlavesSocket.connect(f"tcp://{MASTER_IP}:{updateClientsPort}")
        handleSlavesSocket.setsockopt_string(zmq.SUBSCRIBE, handleSlavesTopic)
        while True:
            receivedMessage=handleSlavesSocket.recv_string()
            topic,message=receivedMessage.split("{")
            message="{"+message
            dictMessage=literal_eval(message)
            address=dictMessage["address"]
            if dictMessage["command"]=="disconnect":
                print(f"disconnecting from slave {address}")
                try:
                    self.readSocket.disconnect(f"tcp://{address}:{serveUserPort}")
                except zmq.ZMQError as e:
                    print("already disconnected", e)   
            if dictMessage["command"]== "connect":
                print(f"connecting to slave {address}")
                self.readSocket.connect(f"tcp://{address}:{serveUserPort}")    


if __name__=="__main__":
    #name=input("Please enter your name")
    #email=input("Please enter your email")
    #password=input("Please enter your password")
    c=Client()
    #print(c.register(name,password,email),"+++++++++++++++++++++++++++")
    for i in range (0,10):
        name=input("Please enter your name")
        password=input("Please enter your password")
        print(c.authenticate(name,password))
    #c.delete(name)
    #print(c.Authenticate(name,password))
    while True:
        pass


   
    



