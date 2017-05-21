import json

from flask import Flask, request, Response
from gevent import spawn
from gevent.queue import Queue

from sse import ServerSentEvent

from crossdomain import crossdomain

from random import randrange

app = Flask(__name__)
subscriptions = []

global_mode = "single"
global_movement = {
    "speed": 0,
    "angle": 0
}

@app.route("/debug")
@crossdomain(origin='*')
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/direction")
@crossdomain(origin='*')
def direction():
    return str(randrange(0, 4))

@app.route("/mode")
@crossdomain(origin='*')
def mode():
    global global_mode

    if not "set" in request.args:
        return global_mode

    global_mode = str(request.args["set"])
    def notify():
        msg = "mode: " + global_mode
        for sub in subscriptions[:]:
            sub.put(msg)

    spawn(notify)

    return global_mode

@app.route("/movement")
@crossdomain(origin='*')
def movement():
    global global_movement

    if not "angle" in request.args and not "speed" in request.args:
        return json.dumps(global_movement)

    if "angle" in request.args:
        global_movement["angle"] = request.args["angle"]

    if "speed" in request.args:
        global_movement["speed"] = request.args["speed"]

    def notify():
        msg = "movement: " + json.dumps(global_movement)
        for sub in subscriptions[:]:
            sub.put(msg)

    spawn(notify)

    return json.dumps(global_movement)

@app.route("/subscribe")
@crossdomain(origin='*')
def subscribe():
    def notify():
        msg1 = "subscriptions: " + str(len(subscriptions))
        msg2 = "mode: " + global_mode
        for sub in subscriptions[:]:
            sub.put(msg1)
            sub.put(msg2)

    def gen():
        q = Queue()
        subscriptions.append(q)
        spawn(notify)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)
            spawn(notify)

    return Response(gen(), mimetype="text/event-stream")
