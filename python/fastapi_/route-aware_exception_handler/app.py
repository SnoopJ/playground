import itertools
import random

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from exceptions import AcmeApplicationException, AnvilError, TNTError
from models import AnvilRequest, TNTRequest
from models import BaseResponse, AnvilResponse, TNTResponse


app = FastAPI()


def _exception_to_response(request, exc) -> JSONResponse:
    error_code = getattr(exc, "error_code", "GENERAL_ERROR")
    cls = request["route"].response_model
    print(f"Using response class {cls.__name__} for error response")
    response = cls(error_info={"error_code": error_code, "route": request["route"].path})
    return JSONResponse(status_code=500, content=response.dict())


# NOTE: this approach sorta-works, but the exception propagates farther than
# expected, causing errors in uvicorn's log, which is a quirk of how
# Starlette's default middleware works. For more details, see:
# https://github.com/encode/starlette/issues/1175

# @app.exception_handler(Exception)
# async def http_exception_handler(request, exc):
#    return _exception_to_response(request, exc)


# workaround for the above
@app.middleware("http")
async def exception_middleware(request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        return _exception_to_response(request, exc)


anvil_excs = iter([
    AcmeApplicationException,
    AnvilError,
    RuntimeError,
])


@app.post("/anvil", response_model=AnvilResponse)
def anvil(req: AnvilRequest):
    exc = next(anvil_excs, None)
    if exc:
        raise exc("An error has occurred")
    sfx = random.choice(["BONK!", "BANG!"])
    return AnvilResponse(sfx=sfx)

tnt_excs = iter([
    AcmeApplicationException,
    TNTError,
    RuntimeError,
])

@app.post("/tnt", response_model=TNTResponse)
def tnt(req: TNTRequest):
    exc = next(tnt_excs, None)
    if exc:
        raise exc("An error has occurred")
    sfx = random.choice(["KABOOM!", "KABLOOEY!"])
    return TNTResponse(sfx=sfx)
