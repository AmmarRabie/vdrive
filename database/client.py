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
import sys
handleSlavesTopic="9999"


serveUserPort=55555 #this port will be used to handle users requests (retrieve, delete,insert)
updateClientsPort=55556 #this port will be used to update clients with the status of slaves
updateSlavesPort=55557 #this port will be used to update slaves when new insertion or delete happens
iamAliveSocketPort=55558
slaveRecoveryHandlerPort=55559 #this port will be used to update the slave with the missed data


class Client:
    def __init__(self):
        """"
        at init establish the connection with the master and slaves script
        """
        self.context = zmq.Context()
        self.insertSocket=self.context.socket(zmq.REQ)
        self.insertSocket.connect(f"tcp://{sys.argv[1]}:{serveUserPort}")
        self.readSocket =self.context.socket(zmq.REQ)
        #self.insertSocket.setsockopt(zmq.RCVTIMEO, 150)
        self.readSocket.setsockopt(zmq.RCVTIMEO, 150)
        for i in range (2,len (sys.argv)):            
            self.readSocket.connect(f"tcp://{sys.argv[i]}:{serveUserPort}")
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
        self.insertSocket.send_json(json.dumps(dictMessage))
        
        try:
            message=self.insertSocket.recv()
            return message
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                #Master is dead!
                return -1


        

    def delete(self,username):
        #Assume that the user already signed in
        dictMessage={
            "Username":username,
            "operation":"delete"
        }
        self.insertSocket.send_json(json.dumps(dictMessage))
        try:
            message=self.insertSocket.recv()
            return message
        except zmq.ZMQError as e:
            if e.errno == zmq.EAGAIN:
                #Master is dead!
                return -1
    def Authenticate(self,username,password):
        dictMessage={
            "Username":username,
            "operation":"authenticate"
        }
        self.readSocket.send_json(json.dumps(dictMessage))
        
        while True:
            try:
                #message will contain the password 
                message=self.readSocket.recv()
                if message == password:
                    return "1"
                return "0"
            except zmq.ZMQError as e:
                print("couldn't receive")
                pass
                #do nothing the client will  try to send to another DB    
    def handleSlaves(self):
        handleSlavesSocket=self.context.socket(zmq.SUB)
        print (sys.argv[1])

        handleSlavesSocket.connect(f"tcp://{sys.argv[1]}:{slaveRecoveryHandlerPort}")
        handleSlavesSocket.setsockopt_string(zmq.SUBSCRIBE, handleSlavesTopic)
        while True:
            message=handleSlavesSocket.recv_json()
            dictMessage=json.loads(message)
            if dictMessage["command"]=="disconnect":
                zmq_disconnect(self.readSocket,dictMessage["address"])
            if dictMessage["command"]== "connect":
                zmq_connect(self.readSocket,dictMessage["address"])    


if __name__=="__main__":
    name=input("Please enter your name")
    email=input("Please enter your email")
    password=input("Please enter your password")
    c=Client()
    print(c.register(name,email,password))
    c.delete(name)
    while True:
        pass


   
    



