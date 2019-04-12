

CHUNK_SIZE = 10000


def readVideo(path):
	file = open(path, "rb")

	data = []
	while True:
		chunk = file.read(CHUNK_SIZE)
		if not chunk:
			break
		data.append(chunk)
	file.close()
	return data



if __name__ == "__main__":
	data = readVideo("zmqHelper.py")
	print(len(data))
	print(data)