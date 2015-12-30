from bottle import route, request, static_file, run
from subprocess import call
import zipfile
import json
import os

MASTER = "http://127.0.0.1:8100"
DLLS_PATH = "C:\\new_dlls\\dlls.zip"
APPLICATION_PATH = "c:\\inetpub\\wwwroot\\"

''' inside the application path will be:
application_name/
    1. Bin
    2. Queries
    2.1. Query
    2.1.1. Id
    2.2. Store
    2.2.1. Id'''


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

    name_app = request.query.applicationName

    cmd_create_pool = 'C:\\Windows\\System32\\inetsrv\\appcmd add apppool /name:{0} /cpu.smpAffinitized:true /processModel.idleTimeout:00:01:00 /processModel.maxProcesses:100 /processModel.shutdownTimeLimit:00:10:00 /processModel.startupTimeLimit:00:10:00 /failure.rapidFailProtection:false'.format(name_app)

    cmd_create_app = 'C:\Windows\\System32\\inetsrv\\appcmd add app /site.name:"Default Web Site" /path:/{0} /physicalPath:{1} /applicationPool:{2}'.format(name_app, APPLICATION_PATH + "\\" + name_app, name_app)

    try:
        call(cmd_create_pool.split())

        call(cmd_create_app.split())

    except:
        return ""

    return "Done!"

if __name__ == '__main__':
    run(host='0.0.0.0', port=8101)
