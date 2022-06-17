from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    retrieve_noun,
)
from app.server.models.word import (
    ResponseModel,
    WordSchema,
)

router = APIRouter()

@router.get("/", response_description="Words retrieved")
async def get_students():
    words = await retrieve_noun()
    if words:
        return ResponseModel(words, "Words data retrieved successfully")
    return ResponseModel(words, "Empty list returned")