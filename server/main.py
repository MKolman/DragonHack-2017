from gevent.wsgi import WSGIServer
from app import app

if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("", 5000), app)
    server.serve_forever()
