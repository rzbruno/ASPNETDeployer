from bottle import route, request, static_file, run
import json
import os

MASTER_IP = "127.0.0.1"

@route('/')
def root():
    return "Node up and running!"

@route('/upload', method='POST')
def upload():
    file = request.files.get('upload')
    file.save("/tmp")
    return "ok"

@route('/applications')
def customers():
    path = "c:\\inetpub\\wwwroot\\"
    directories = [d for d in os.listdir(path) if os.path.isdir(path+'/'+d)]
    d = {}
    for i in range(len(directories)):
        d[i] = directories[i]

    return json.dumps(d)

if __name__ == '__main__':
    run(host='0.0.0.0', port=8101)
