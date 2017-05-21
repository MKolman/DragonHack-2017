import json
import time
import math

from flask import Flask, request, Response
from gevent import spawn
from gevent.queue import Queue

from sse import ServerSentEvent

from crossdomain import crossdomain

from random import choice

app = Flask(__name__)
subscriptions = []
subscription_global_id = 1

global_mode = "single"
global_movement = {
    "speed": 0,
    "angle": 0
}

global_movement_multi = dict()
global_last_multi = time.time()

@app.route("/debug")
@crossdomain(origin='*')
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/direction")
@crossdomain(origin='*')
def direction():
    global global_last_multi
    global global_movement_multi
    global global_movement

    if global_mode != "single" and len(global_movement_multi.keys()):
        old = global_last_multi
        new = time.time()

        if new - global_last_multi > 1000:
            global_last_multi = new

        if global_mode == "democracy":
            x = 0
            y = 0
            for item in global_movement_multi.values():
                x += item["speed"] * math.cos(- item["angle"] / 180 * math.pi)
                y += item["speed"] * math.sin(- item["angle"] / 180 * math.pi)
            x /= len(global_movement_multi)
            y /= len(global_movement_multi)

            theta = -math.atan2(y, x) / math.pi * 180
            if theta < 0:
                theta += 360

            r = math.sqrt(x*x + y*y)

            global_movement = {
                "speed": int(r),
                "angle": int(theta)
            }
        elif global_mode == "anarchy":
            global_movement = choice(list(global_movement_multi.values()))

        global_movement_multi = dict()

        def notify():
            msg = "movement: " + json.dumps(global_movement)
            for sub in subscriptions[:]:
                sub.put(msg)

        spawn(notify)

    return str(global_movement["speed"]) + " " + str(global_movement["angle"])

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
    global global_movement_multi

    if not "angle" in request.args and not "speed" in request.args:
        return json.dumps(global_movement)

    if global_mode != "single" and "global_id" in request.args and "angle" in request.args and "speed" in request.args:
        global_movement_multi[int(request.args["global_id"])] = {
            "angle": int(request.args["angle"]),
            "speed": int(request.args["speed"])
        }
    else:
        if "angle" in request.args:
            global_movement["angle"] = int(request.args["angle"])

        if "speed" in request.args:
            global_movement["speed"] = int(request.args["speed"])

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
            sub.put("global_id: " + str(sub.global_id))
            sub.put(msg1)
            sub.put(msg2)

    def gen():
        global subscription_global_id

        q = Queue()
        q.global_id = subscription_global_id
        subscription_global_id += 1
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
