from flask import Flask, request, Response
from gevent import spawn
from gevent.queue import Queue

from sse import ServerSentEvent

from crossdomain import crossdomain

from random import randrange

app = Flask(__name__)
subscriptions = []

pixels = [" " for i in range(9)]
current_player = "x"

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/direction")
def direction():
    return str(randrange(0, 4))

@app.route("/subscribe")
@crossdomain(origin='*')
def subscribe():
    def notify():
        msg = str(len(subscriptions))
        for sub in subscriptions[:]:
            sub.put(msg)

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
