from bottle import route, run, response
import json

NODE_IP = json.loads('{"node1": "0.0.0.0", "node2": "1.1.1.1", "node3": "2.2.2.2"}')

@route('/')
def root():
    return "Master up and running!"

@route('/nodes')
def getNodes():
    return json.dumps(NODE_IP)

if __name__ == '__main__':
    run(host='0.0.0.0', port=8100)

