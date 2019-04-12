import sys
sys.path.append('.')
from fileexplorer import FileExplorer
from downloader import Downloader
from uploader import Uploader
from argparse import ArgumentParser

def getUserFunction():
    """
        get user action, now just get it from command line parameters
    """
    function = sys.argv[1]
    return {"ls": "fileexplorer", "d": "downloader", "u":"uploader"}.get(function)


def main():
    print("Hi, I'am a client :)")
    
    action = getUserFunction()
    # TODO: get here the username, password and query the user id => then generate a token
    userToken = "asjfjnfksndgknskgnskngrkgneokmgr"
    if action == "fileexplorer":
        fileExplorer = FileExplorer()
        fileExplorer.explore(userToken)
    if action == "downloader":
        downloader = Downloader()
        # ...
    
if __name__ == "__main__":
    main()