from fastapi import FastAPI
from server.routes.word import router as WordRouter
from server.routes.noun import router as NounRouter
from server.routes.aggregated import router as AggregatedRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from server.database import delete_old_word, update_type, aggregate_word

app = FastAPI()
app.include_router(WordRouter, tags=["Word"], prefix="/word")
app.include_router(NounRouter, tags=["Noun"], prefix="/noun")
app.include_router(AggregatedRouter, tags=["Aggregated"], prefix="/aggregated")


origins = origins = [
    "https://news-trend.netlify.app",
    "http://localhost:3000",
    "news-trend.netlify.app",
    "http://news-trend.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # Once a day
async def clean_up_data() -> None:
    await delete_old_word()
    await update_type()
    await aggregate_word()
    return


@app.get("/")
async def root():
    # delete_old_word()
    return {"message": "Hello World"}
