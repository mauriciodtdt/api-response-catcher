from flask import Flask, request, Response, jsonify, render_template
from gevent import pywsgi
from flask_sockets import Sockets
#from geventwebsocket.handler import WebSocketHandler
app = Flask(__name__)
sockets = Sockets(app)

@app.route('/listen', methods=['POST'])
def listen():
  name = request.json()
  return Response(name, mimetype='text/event-stream', content=name)

@app.route('/<name>')
def user(name):
    return render_template("index.html", content=name)

@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)


@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('localhost', 5000), app)
    server.serve_forever()

# Copy of http://stackoverflow.com/a/20104705
# from flask import Flask, render_template
# from flask_sockets import Sockets

# app = Flask(__name__)
# app.debug = True

# sockets = Sockets(app)

# @sockets.route('/echo')
# def echo_socket(ws):
#     while True:
#         message = ws.receive()
#         ws.send(message[::-1])

# @app.route('/')
# def hello():
#     return 'Hello World!'

# @app.route('/echo_test', methods=['GET'])
# def echo_test():
#     return render_template('echo_test.html')

# if __name__ == '__main__':
#     app.run()