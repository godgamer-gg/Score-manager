import sys
from pathlib import Path
import logging
from typing import Union

from fastapi import FastAPI

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))
from ScoreManager import ScoreManager

app = FastAPI()

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

@app.post("/steamscore/id")
async def get_steamscoreFromID(user: str, steamID: str):
    score = scoreManager.calculateSteamScores(steamID)
    return {score}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}