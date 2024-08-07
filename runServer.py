# TO RUN THIS FILE python3 -m uvicorn runServer:app --reload


import sys
from pathlib import Path
import logging
from typing import Union

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

from scoring.ScoreManager import ScoreManager


logging.basicConfig(level=logging.INFO)

scoreManager = ScoreManager()


# init scoremanager on startup
async def lifespan(app: FastAPI):
    logger = logging.getLogger("uvicorn.info")
    logger.info('scoreManager init')
    yield
    scoreManager.shutdown()
    logger.info("Shut down scoremanager")

app = FastAPI(lifespan=lifespan)

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

@app.middleware("http")
async def log_request(request, call_next):
    logger = logging.getLogger("uvicorn.info")
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    return response

# no idea why this is here
# path_root = Path(__file__).parents[1]
# sys.path.append(str(path_root))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello")
def say_hello():
    return {"Hello!"}

@app.get("/steamscore/steamCode/{steam_id}")
async def get_steamscoreFromID(steam_id: str):
    print(steam_id)
    score = scoreManager.calculateSteamScoresForGuest(steam_id)
    return {score}

@app.get("/steamscore/friendCode/{friend_code}")
async def get_seamscoreFromFriendCode(friend_code: str):
    print(friend_code)



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


