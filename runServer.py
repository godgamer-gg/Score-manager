# TO RUN THIS FILE python3 -m uvicorn runServer:app --reload


import sys
from pathlib import Path
import logging
from typing import Union

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from ScoreManager import ScoreManager

app = FastAPI()

# app.mount("/", StaticFiles(directory="../frontend/nextjs-blog/", html=True), name="static")


scoreManager = None

# init scoremanager on startup
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO)
    scoreManager = ScoreManager()
    logging.info('scoreManager init')
    yield
    scoreManager.shutdown()
    logging.info("Shut down scoremanager")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello")
def say_hello():
    return {"Hello!"}

@app.get("/steamscore/steamCode/{steam_id}")
async def get_steamscoreFromID(steam_id: str):
    print(steam_id)
    score = scoreManager.calculateSteamScores(steam_id)
    return {score}

@app.get("/steamscore/friendCode/{friend_code}")
async def get_seamscoreFromFriendCode(friend_code: str):
    print(friend_code)



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}