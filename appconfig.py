TOKEN_SECRET = "jndsjfhslaLkGwkfjnlsSDGHOJdasf"


N = 3 # number of replicas
T = 1 # every one second
P = 5 # number of processes

TRACKER_IP = "127.0.0.1" # the master tracker machine ip (in real world, this is a static ip)
TRACKER_PORTS = ("7000",) # for the tracker machine, there is a lot of ports that client can communicated with
TRACKER_PORTS_KEEPERS = ("8000",) # ports that data keepers communicate with
#? assume that every machine have the same ports
DATA_KEEPER_IPS = ("127.0.0.1", )
DATA_KEEPER_PORTS = ("6000",) # for each data keeper machine there is a list of propably available ports


TRACKER_ALIVE_PORT = "7500"

DATA_KEEPER_ALIVE_SEND_RATE = 1 # send every one second
DATA_KEEPER_TIME_OUT = DATA_KEEPER_ALIVE_SEND_RATE + 1 # one second more, depends on the network traffic