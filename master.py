from bottle import route, run, response
import json

NODE_IP = json.loads('{"node1": "127.0.0.1"}')

@route('/')
def root():
    return "Master up and running!"

@route('/nodes')
def getNodes():
    return json.dumps(NODE_IP)

if __name__ == '__main__':
    run(host='0.0.0.0', port=8100)

