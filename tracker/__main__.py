import sys
sys.path.append('.')
from fileexplorer import FileExplorer

def main(port):
    print("Hi, i am tracker server on port " + port)
    FileExplorer(port).explore()


if __name__ == "__main__":
    main(sys.argv[1])