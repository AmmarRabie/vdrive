import datetime
import jwt
from appconfig import TOKEN_SECRET
import socket as pysocket

def readVideo(path):
	CHUNK_SIZE = 10000
	file = open(path, "rb")

	data = []
	while True:
		chunk = file.read(CHUNK_SIZE)
		if not chunk:
			break
		data.append(chunk)
	file.close()
	return data


def writeVideo(video, path):
	file = open(path, "wb")

	for item in video:
		file.write(item)

	file.close()



def getCurrMachineIp():
	# TODO: remove the following line
	# return "127.0.0.1"
	# import socket
	s = pysocket.socket(pysocket.AF_INET, pysocket.SOCK_DGRAM)
	try:
	    # doesn't even have to be reachable
	    s.connect(('10.255.255.255', 1))
	    IP = s.getsockname()[0]
	except:
	    IP = '127.0.0.1'
	finally:
	    s.close()
	return IP

def generateToken(username, password):
	return jwt.encode(
        {'username': username, "pass": password, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=10000)},
        TOKEN_SECRET)

def decodeToken(token):
	try:
		userInfo = jwt.decode(token, TOKEN_SECRET)
		return userInfo["username"], userInfo["pass"]
	except Exception as e:
		print(e)
		return None, None

if __name__ == "__main__":
	data = readVideo("dummyvideo.mp4")
	print(len(data))
	writeVideo(data, "new.mp4")