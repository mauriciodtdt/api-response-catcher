from gevent import monkey; monkey.patch_all()
from flask import Flask, Response, render_template, stream_with_context, redirect, request, jsonify
from gevent.pywsgi import WSGIServer
import json
import time
from datetime import datetime

app = Flask(__name__)
message_by_user = {}
message_list = []
counter = 100


@app.route("/")
def index():
    return f"Please append your name to the URL"


@app.route('/<user>')
def user(user):
    return render_template("user.html", content=str(user))


@app.route("/<user>/listen")
def listen(user):
    def respond_to_client():
        global message_list
        message_list = message_by_user.get(user) if user in message_by_user.keys() else []
        if message_list:
            _data = json.dumps({"timestamp": datetime.utcnow().strftime("%b %d %Y - %H:%M:%S"),
                                "callback_msg": message_list.pop()})
            return f"id: 1\ndata: {_data}\nevent: online\n\n"
    return Response(respond_to_client(), mimetype='text/event-stream')


@app.route('/<user>/receive', methods=['POST'])
def receive(user):
    _data = request.json
    message_list: list = message_by_user.get(user) if user in message_by_user.keys() else []
    message_list.append(_data)
    message_by_user.update({user: message_list})
    print(user)
    print(f'\nTotal messages: {len(message_list)} for user: {user}')
    return _data


##############################
if __name__ == "__main__":
  http_server = WSGIServer(("localhost", 5001), app)
  http_server.serve_forever()