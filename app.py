from flask import Flask, request, jsonify, render_template
from gevent import pywsgi
#from geventwebsocket.handler import WebSocketHandler
app = Flask(__name__)

@app.route('/getmsg/', methods=['POST'])
def respond():
    # Retrieve the name from url parameter
    name = request.json()

    # For debugging
    print(f"Got response:\n{name}")

# A welcome message to test our server
@app.route('/')
def index():
    return "Hello this is the main page <h1>HELLO<h1>"

@app.route("/<name>", methods=['POST'])
def user(name):
    body_api = request.json()
    return render_template("index.html", content=body_api)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('localhost', 5000), app)
    server.serve_forever()
