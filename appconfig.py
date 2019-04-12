


N = 3 # number of replicas
T = 1 # every one second
P = 5 # number of processes

TRACKER_IP = "192.168.1.8" # the master tracker machine ip (in real world, this is a static ip)
TRACKER_PORTS = ("8082", "8081", "8080",) # for the tracker machine, there is a lot of ports that can be communicated with

#? assume that every machine have the same ports
DATA_KEEPER_IPS = ("192.168.1.8",) # append here the ips of all the data keeper nodes(machines)
DATA_KEEPER_PORTS = ("8080", "8081", "8082",) # for each data keeper machine there is a list of propably available ports