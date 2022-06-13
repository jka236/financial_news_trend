from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from app.server.database import (
    retrieve_word,
    add_word
)
from app.server.models.word import (
    ErrorResponseModel,
    ResponseModel,
    WordSchema,
)

router = APIRouter()


@router.post("/", response_description="word data added into the database")
async def add_word_data(word: WordSchema = Body(...)):
    word = jsonable_encoder(word)
    new_word = await add_word(word)
    return ResponseModel(new_word, "word added successfully.")

@router.get("/", response_description="Words retrieved")
async def get_students():
    words = await retrieve_word()
    if words:
        return ResponseModel(words, "Words data retrieved successfully")
    return ResponseModel(words, "Empty list returned")