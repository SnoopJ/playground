"""
This sample shows how to run a uvicorn server that attempts to bind to a
canonical port and falls back on an ephemeral port, in a way that can be
reported to another dependent process.
"""
from fastapi import FastAPI
import uvicorn
import socket
import time


app = FastAPI()

@app.get("/")
def route():
    """Dummy route to illustrate that the server still works"""
    return "Hello :)"


def _get_socket() -> socket.socket:
    CANONICAL_PORT = -1  # NOTE:value of -1 is to guarantee a failure here in the sample
    HOST = "localhost"
    try:
        sock = socket.create_server((HOST, CANONICAL_PORT))
    except:
        print(f"Could not bind to {(HOST, CANONICAL_PORT)}, binding ephemeral port")
        sock = socket.create_server((HOST, 0))

    return sock


if __name__ == "__main__":
    config = uvicorn.Config(app)
    server = uvicorn.Server(config=config)
    sock = _get_socket()

    # Here, I can communicate the actual port being used to another process
    # that depends on my server by e.g. writing to a file

    print(f"Starting server on {sock.getsockname()}")
    server.run(sockets=[sock])
