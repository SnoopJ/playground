"""
This sample shows how to run a uvicorn server that binds to multiple addresses,
motivated by a problem at work where a service bound only to `localhost` but the
downstream sometimes instead sent its requests to the hostname (bound to 127.0.1.1 on
Debian systems)
"""
from __future__ import annotations
from fastapi import FastAPI
import uvicorn
import socket
import time


app = FastAPI()

@app.get("/")
def route():
    """Dummy route to illustrate that the server still works"""
    return "Hello :)"


def _sockets() -> list[socket.socket]:
    PORT = 8080
    HOSTS = ["localhost", socket.gethostname()]
    socks = []
    for host in HOSTS:
        sock = socket.create_server((host, PORT))
        socks.append(sock)

    return socks


if __name__ == "__main__":
    config = uvicorn.Config(app)
    server = uvicorn.Server(config=config)
    socks = _sockets()

    for sock in socks:
        print(f"Using socket {sock.getsockname()}")
    server.run(sockets=socks)
