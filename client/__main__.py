import sys
sys.path.append('.')
from fileexplorer import FileExplorer
from downloader import Downloader
from uploader import Uploader
from argparse import ArgumentParser
from os import system as cmd
from random import randint
from database.client import Client as DbClint
from client import Client as FSClient
from common.util import generateToken

class Client(DbClint, FSClient):
    def __init__(self):
        DbClint.__init__(self)
        FSClient.__init__(self)

    def interactiveAuthUser(self):
        """
            this function is to authenticate user interactively from terminal
        """
        mes = \
        """Dear client, to be able to user this system, you should sign in first
        1) I have an account
        2) create new account
        """
        action = input(mes)
        while not (action == "1" or action == "2"):
            action = input(mes)
        if action == "1":
            print("great, enter your credentials below")
            username = input("username: ")
            password = input("password: ")
            isValidUser = self.authenticate(username, password)
            print(isValidUser)
            while (not isValidUser):
                print("invalid user")
                tryAgain = input("try again ?y/n").upper()
                if tryAgain == "Y":
                    username = input("username: ")
                    password = input("password: ")
                    isValidUser = self.authenticate(username, password)
                    print("invalid user", isValidUser)
                else:
                    return False
            return True
        elif action == "2":
            username = input("username: ")
            email = input("email: ")
            password = input("password: ")
            confirmPass = input("confirm password: ")
            while (password != confirmPass):
                password = input("password: ")
                confirmPass = input("confirm password: ")

            return self.register(username, password, email)

    def interactiveUserFunction(self):
        """
            this function is to execute a user function interactively from terminal
        """
        name, kwargs = self._getUserFunction()
        if (not name):
            return False
        if (name == 'logout'):
            return True

        getattr(self, name)(self.token, **kwargs)
        return name == 'delete'

    def _getUserFunction(self):
        """
            get user action, now just get it from command line interacting
        """
        mes = \
        """Please choose one of the functions below, just enter the number of it
        1) show me my files
        2) download a file
        3) upload new file
        4) delete my account
        5) log out
        """
        function = input(mes)
        name = ""
        kwargs = {}
        if function == "1":
            name = "listFiles"
        elif function == "2":
            name = "downloadFile"
            fileName = input("what is the file name ")
            kwargs = dict(fileName = fileName)
        elif function == "3":
            name = "uploadLocalFile"
            filePath = input("what is the file path ")
            kwargs = dict(filePath = filePath)
        elif function == "4":
            name = "delete"
            print("ok, mesh mohm, e7na asln mesh 3aizink 3ndna fel database")
        elif function == "5":
            name = "logout"
        return name, kwargs

    def authenticate(self, username, password):
        # override super class to update curr user
        self.token = DbClint.authenticate(self, username, password)
        return self.token
    def register(self, username, password, email):
        self.token = DbClint.register(self, username, password, email)
        print("token recieved from the database is", self.token)
        return self.token

if __name__ == "__main__":
    c1 = Client()
    exit = False
    while(not exit):
        valid = False
        while(not valid):
            valid = c1.interactiveAuthUser()
        signout = False
        while(not signout):
            signout = c1.interactiveUserFunction()
        # exit = str(input("do you want to exit Y/N")).capitalize() == 'Y'