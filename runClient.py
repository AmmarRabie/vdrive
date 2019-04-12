import os
import random

if (len(os.sys.argv) < 2):
    print("provide a function for the client")
    os.system("pause")
    pass
clientNumber = random.randint(1, 1000)
os.system('start "client %s" python client ' % clientNumber + os.sys.argv[1])

os.system("pause")