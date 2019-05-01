TOKEN_SECRET = "jndsjfhslaLkGwkfjnlsSDGHOJdasf"
PYTHON_PATH = "D:/workspace/TYFDS/venv/Scripts/python.exe"

N = 3 # number of replicas
T = 1 # every one second
P = 5 # number of processes

TRACKER_IP = "192.168.43.231" # the master tracker machine ip (in real world, this is a static ip)
TRACKER_PORTS = ("7000", "7001", "7002") # for the tracker machine, there is a lot of ports that client can communicated with
TRACKER_PORTS_KEEPERS = ("8000",) # ports that data keepers communicate with
#? assume that every machine have the same ports
DATA_KEEPER_IPS = ("192.168.43.231", "192.168.43.188")
DATA_KEEPER_PORTS = ("6000", "6001", "6002", "6003", "6004", "6005", "6006", "6007", "6008", "6009" ) # for each data keeper machine there is a list of propably available ports
TRACKER_TO_KEEPERS_PORTS = ("6500",) # ports that tracker communicate with data keeper to till it that there is a replication required

TRACKER_ALIVE_PORT = "7500"

DATA_KEEPER_ALIVE_SEND_RATE = 1 # send every one second
DATA_KEEPER_TIME_OUT = DATA_KEEPER_ALIVE_SEND_RATE + 1 # one second more, depends on the network traffic

KEEPERS_TO_KEEPERS_REPL_PORT = "9000" # keepers to keepers reqrep port for replication process, we are now handle at maximum two at once


# database config
MASTER_IP = "192.168.43.231"
# SLAVES_IPS = ["192.168.43.188", "192.168.43.206"]
SLAVES_IPS = []
serveUserPort=55555 #this port will be used to handle users requests (retrieve, delete,insert)
updateClientsPort=55556 #this port will be used to update clients with the status of slaves
updateSlavesPort=55557 #this port will be used to update slaves when new insertion or delete happens
iamAliveSocketPort=55558
slaveRecoveryHandlerPort=55559 #this port will be used to update the slave with the missed data
