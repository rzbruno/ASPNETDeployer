import requests
import json
import os
import sys

MASTER = "http://127.0.0.1:8100"

NODES = ""
try:
    NODES = (requests.get(MASTER + "/nodes")).text
    NODES = json.loads(NODES)
except:
    print("Ops.. Couldn't retrieve master server.")

def cliUsage():
    print("Accepted usage:")
    print("client.py 1: get all aplication names")
    print("client.py 2: update all applications")
    print("client.py 3: update single <application name>")
    print("client.py 4: deploy <application name>")

def getNodes():
    for key,value in NODES.items():
        print("{}:{}".format(key,value))

def updateAll():
    print("updateAll")

    return
    binPath = input("Enter with the absolute path of the file dlls.zip: ")

    if not (os.path.isfile(binPath)):
        print("Sorry! you need the full path. Ex.: c:\\dlls.zip")
        return

    for node in NODES:
        url = "http://" + node + ":8101"
        files = {'upload': open('dlls.zip', 'rb')}
        r = requests.post(url + "/upload", files=files)
        #r.text
        r = requests.get(url + "/syncAll")
        #r.text

def updateSingle():
    print("updateSingle")

def deployApplication():
    print("deployApplication")

if __name__ == '__main__':

    if len(NODES) > 0:

        if len(sys.argv) != 2 or sys.argv[1] not in ("1","2","3","4",): cliUsage()

        elif sys.argv[1] == "1": getNodes()
        elif sys.argv[1] == "2": updateAll()
        elif sys.argv[1] == "3": updateSingle()
        elif sys.argv[1] == "4": deployApplication()

