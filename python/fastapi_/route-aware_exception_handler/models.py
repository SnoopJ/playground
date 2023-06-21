from typing import Optional

from pydantic import BaseModel, Field
from fastapi.responses import Response


class AnvilRequest(BaseModel):
    weight: int


class TNTRequest(BaseModel):
    yield_: int = Field(alias="yield")



class BaseResponse(BaseModel):
    sfx: str = ""
    flattened: bool = False
    exploded: bool = False

    error_info: Optional[dict]


class AnvilResponse(BaseResponse):
    sfx: str = "BONK!"
    flattened: bool = True


class TNTResponse(BaseResponse):
    sfx: str = "KABOOM!"
    exploded: bool = True
