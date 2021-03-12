# from flask import Flask, request, Response, jsonify, render_template
# from gevent import pywsgi
# from flask_sockets import Sockets
# #from geventwebsocket.handler import WebSocketHandler
# app = Flask(__name__)
# sockets = Sockets(app)

# @app.route('/listen', methods=['POST'])
# def listen():
#     _data = request.json
#     # return jsonify(data)
#     def respond_to_client():
#         while True:
#             yield f"id: 1\ndata: {_data}\nevent: online\n\n"
#             time.sleep(0.5)
# #   return Response(respond_to_client(), mimetype='text/event-stream')
#         return jsonify(_data)
#     return respond_to_client()

# @app.route('/<name>')
# def user(name):
#     return render_template("index.html", content=name)

# @sockets.route('/echo')
# def echo_socket(ws):
#     while not ws.closed:
#         message = ws.receive()
#         ws.send(message)


# @app.route('/')
# def hello():
#     return 'Hello World!'

# if __name__ == '__main__':
#     server = pywsgi.WSGIServer(('localhost', 5000), app)
#     server.serve_forever()

# # Copy of http://stackoverflow.com/a/20104705
# # from flask import Flask, render_template
# # from flask_sockets import Sockets

# # app = Flask(__name__)
# # app.debug = True

# # sockets = Sockets(app)

# # @sockets.route('/echo')
# # def echo_socket(ws):
# #     while True:
# #         message = ws.receive()
# #         ws.send(message[::-1])

# # @app.route('/')
# # def hello():
# #     return 'Hello World!'

# # @app.route('/echo_test', methods=['GET'])
# # def echo_test():
# #     return render_template('echo_test.html')

# # if __name__ == '__main__':
# #     app.run()

from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template, stream_with_context, redirect, request, jsonify
from gevent.pywsgi import WSGIServer
import json
import time
from datetime import datetime

app = Flask(__name__)
message_list = []
counter = 100

##############################
@app.route("/index")
def index():
  return render_template("index.html")

############################
@app.route("/listen")
def listen():
  def respond_to_client():
    global counter
    if message_list:
        _data = json.dumps({"timestamp": datetime.utcnow().strftime("%H:%M:%S"), "callback_msg":message_list.pop()})
        return f"id: 1\ndata: {_data}\nevent: online\n\n"
  return Response(respond_to_client(), mimetype='text/event-stream')

@app.route('/receive', methods=['POST'])
def receive():
    _data = request.json
    message_list.append(_data)
    print(f'\nTotal: {len(message_list)}')
    return _data
      
# @app.route('/listen')
# def listen():
#     def respond_to_client():
#         if message_list:
#             yield f"id: 1\ndata: {message_list.pop()}\nevent: online\n\n"
#     lt = respond_to_client()
#     print(f'Yielding: {lt}')
#     return Response(lt, mimetype='text/event-stream')

@app.route('/receive', methods=['POST'])
def signUpUser():
    user =  request.data;
    return json.dumps({'status':'OK','user':user});

@app.route('/interactive/')
def interactive():
	return render_template('interactive.html')


@app.route('/background_process')
def background_process():
	try:
		lang = request.args.get('proglang', 0, type=str)
		if lang.lower() == 'python':
			return jsonify(result='You are wise')
		else:
			return jsonify(result='Try again.')
	except Exception as e:
		return str(e)



##############################
if __name__ == "__main__":
#   app.run(port=5000, debug=True)
  http_server = WSGIServer(("localhost", 5000), app)
  http_server.serve_forever()