from fastapi import FastAPI
from app.server.routes.word import router as WordRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(WordRouter, tags=["Word"], prefix="/word")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}
