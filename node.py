from bottle import route, request, static_file, run
from subprocess import call
import zipfile
import json
import os

MASTER = "http://127.0.0.1:8100"
DLLS_PATH = "C:\\new_dlls\\dlls.zip"
APPLICATION_PATH = "c:\\inetpub\\wwwroot\\"

@route('/')
def root():
    return "Node up and running!"

@route('/upload', method='POST')
def upload():
    file = request.files.get('upload')
    file.save(DLLS_PATH, True)
    return "Done."

def getApplicationList():
    return [d for d in os.listdir(APPLICATION_PATH) if os.path.isdir(APPLICATION_PATH+'/'+d)]

@route('/applications')
def customers():
    directories = getApplicationList()
    d = {}
    for i in range(len(directories)):
        d[i] = directories[i]

    return json.dumps(d)

@route('/syncAll')
def syncAll():

    zip_ref = zipfile.ZipFile(DLLS_PATH, 'r')

    for application in getApplicationList():
        zip_ref.extractall(application + '/bin/')

    zip_ref.close()

    return "Done."

@route('/syncOne')
def syncOne():
    zip_ref = zipfile.ZipFile(DLLS_PATH, 'r')

    applicationName = request.query.applicationName

    if applicationName != "":
        zip_ref.extractall(applicationName + '/bin/')

    zip_ref.close()

    return "Done."

@route('/deployApplication')
def deployApplication():

    name = request.query.applicationName

    cmd = "appcmd add app /site.name: {0} /path: {1} /physicalPath: {2}".format(name, name, APPLICATION_PATH + "\\" + name)

    try:
        call(cmd.split())
    except:
        return ""

    return "Done!"

if __name__ == '__main__':
    run(host='0.0.0.0', port=8101)
