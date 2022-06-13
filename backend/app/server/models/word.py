from pydantic import BaseModel, Field


class WordSchema(BaseModel):
    article_title: str = Field(...)
    class Config:
        schema_extra = {
            "example": {
                "article_title": "example",
            }
        }
        
        
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}