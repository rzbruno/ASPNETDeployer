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


def cli_usage():
    print("Accepted usage:")
    print("client.py 1: show available nodes")
    print("client.py 2: show applications by nodes")
    print("client.py 3: update all applications")
    print("client.py 4: update single <application name>")
    print("client.py 5: deploy <application name>")


def show_nodes():

    for key,value in NODES.items():
        print("{}:{}".format(key,value))


def show_application_by_node():

    try:
        for nodeName, nodeIP in NODES.items():
            request = requests.get("http://" + nodeIP + ":8101/applications").text
            applications = json.loads(request)

            for k in applications:
                print("Node: {} - Application: {}".format(nodeName, applications[k]))
    except:
        print("Whoa, something went wrong.")


def get_update_path():
    dlls_path = input("Enter with the absolute path of the file dlls.zip.\r\nExample: d:\\projects\\X\\bin\\dlls.zip\r\n\r\n")

    if not os.path.isfile(dlls_path):
        print("Not a valid absolute path to a file.")
        return ""

    name, ext = os.path.splitext(dlls_path)

    if ext != '.zip':
        print("The only accepts extension is .zip")
        return ""

    return dlls_path


def update_all():

    try:
        dlls_path = get_update_path()

        if dlls_path == "":
            return

        for key in NODES:
            url = "http://" + NODES[key] + ":8101/upload"
            file = {'upload': open(dlls_path, 'rb')}
            r = requests.post(url, files=file)

            if r.status_code == 200:
                r = requests.get(url + "/syncAll")
                if r.status_code == 200:
                    print("All applications were synchronized.")
                else:
                    print("Something went wrong to synchronize applications. Returned code/result: " + r.status_code + " - " + r.text)
            else:
                print("Whoa, something went wrong to upload. Returned code/result: " + r.status_code + " - " + r.text)
    except:
        print("Whoa, something went wrong.")


def update_single(applicationName=None, dlls_path=None):

    if dlls_path is None:
        dlls_path = get_update_path()
        if dlls_path == "":
            return

    if applicationName is None:
        applicationName = input("Enter with the exact name of the application to update: ")

    for nodeName, nodeIP in NODES.items():
        request = requests.get("http://" + nodeIP + ":8101/applications").text
        applications = json.loads(request)

        for k in applications:
            if applications[k] == applicationName:
                url = "http://" + nodeIP + ":8101/upload"
                file = {'upload': open(dlls_path, 'rb')}
                r = requests.post(url, files=file)

                if r.status_code == 200:
                    r = requests.get(url + "/syncOne?applicationName=" + applicationName)
                    print("The {0} {1} synchronized.".format(applicationName, "was" if r.status_code == 200 else "was not"))
                else:
                    print("The upload was found, but upload has failed: Return: {0} - {1}".format(r.status_code, r.text))


def deploy_application():

    server_name = "Enter with the exact server name: "

    if server_name == "":
        return

    dlls_path = get_update_path()

    if dlls_path == "":
        return

    applicationName = "Enter with the application name: "

    if applicationName != "":
        r = requests.get("http://" + NODES.get(server_name) + ":8101/deployApplication?applicationName=" + applicationName)
        if r.status_code == 200:
            update_single(applicationName, dlls_path)

if __name__ == '__main__':

    if len(NODES) > 0:

        if len(sys.argv) != 2 or sys.argv[1] not in ("1","2","3","4","5"): cli_usage()

        elif sys.argv[1] == "1": show_nodes()
        elif sys.argv[1] == "2": show_application_by_node()
        elif sys.argv[1] == "3": update_all()
        elif sys.argv[1] == "4": update_single()
        elif sys.argv[1] == "5": deploy_application()

