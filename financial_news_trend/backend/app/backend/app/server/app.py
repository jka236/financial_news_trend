from fastapi import FastAPI
from server.routes.word import router as WordRouter
from server.routes.noun import router as NounRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from server.database import delete_old_word

app = FastAPI()
app.include_router(WordRouter, tags=["Word"], prefix="/word")
app.include_router(NounRouter, tags=["Noun"], prefix="/noun")

origins = ["https://news-trend.vercel.app/", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # Once a day
async def remove_old_data() -> None:
    await delete_old_word()
    return


@app.get("/")
async def root():
    # delete_old_word()
    return {"message": "Hello World"}
