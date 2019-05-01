"""
Run this file if you want a tracker process that deal with data keepers nodes requests

paramaters to this script if be run directly:
1- port that the tracker node will bind for

Datakeeper request should be a json object like
{
    "function": "download", # download mean the data keeper is downloaded a file from the client, upload mean data node has just uploaded a file to the client
    "filename": "name of the file downloaded" # only give this property if the function is downloaded
    "username" "the user who is uploaded the file",
    "ip": "the ip of the data keeper machine", # should be given
    "port": "the port of the process", # should be given
}
"""
import sys
sys.path.append("../")
import zmq
from common.zmqHelper import zhelper
from common.util import getCurrMachineIp
from trackerdbcontroller import TrackerDBController as Db

def main(port):
    ip = getCurrMachineIp()
    socket = zhelper.newServerSocket(zmq.REP, ip, port)
    db = Db("TrackerDB")
    while(True):
        nodeRequestData = socket.recv_json()
        socket.send_string("ACK")
        handle(nodeRequestData, db)

def handle(data, db):
    if data.get("function") == "download": # new file was created
        filename, username = data.get("filename"), data.get("username")
        print(f"action: inserting file {username}/{filename} into the database")
        # db.insertFile(username, filename, getCurrMachineIp())
        db.insertFile(username, filename, data.get("ip"))        
    if data.get("function") in ("download", "upload"):
        ip, port = data.get("ip"), data.get("port")
        # free port
        print(f"freeing {ip}:{port}")
        db.setNodeBusyState(ip, port, isBusy=False) 


if __name__ == "__main__":
    import sys
    from appconfig import TRACKER_PORTS_KEEPERS
    port = TRACKER_PORTS_KEEPERS[0]
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    main(port)
