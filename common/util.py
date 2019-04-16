
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


def writeVideo(video, path):
	file = open(path, "wb")

	for item in video:
		file.write(item)

	file.close()



if __name__ == "__main__":
	data = readVideo("dummyvideo.mp4")
	print(len(data))
	writeVideo(data, "new.mp4")