from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    retrieve_aggregated_noun,
)
from server.models.word import (
    ResponseModel,
    WordSchema,
)

router = APIRouter()

@router.get("/", response_description="Words retrieved")
async def get_aggregated():
    words = await retrieve_aggregated_noun()
    if words:
        return ResponseModel(words, "Words data retrieved successfully")
    return ResponseModel(words, "Empty list returned")