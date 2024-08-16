# TO RUN THIS FILE python3 -m uvicorn runServer:app --reload


import sys
from pathlib import Path
import logging
from typing import Union

from fastapi import FastAPI, Header, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# from scoring.scoreManager import ScoreManager
from manager import Manager


logging.basicConfig(level=logging.INFO)

manager = Manager()


# init scoremanager on startup
# post refactoring this is probably no longer necessary, leaving in case it's needed
async def lifespan(app: FastAPI):
    logger = logging.getLogger("uvicorn.info")
    logger.info('scoreManager init')
    yield
    manager.scoreManager.shutdown()
    logger.info("Shut down scoremanager")

security = HTTPBasic()
app = FastAPI(lifespan=lifespan, dependencies=[Depends(security)])

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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello")
def say_hello():
    return {"Hello!"}

@app.get("/steamscore/steamCode/{steam_id}")
async def get_steamscoreFromID(steam_id: str):
    print(steam_id)
    score = manager.scoreManager.calculateSteamScoresForGuest(steam_id)
    return {score}

@app.get("/steamscore/friendCode/{friend_code}")
async def get_steamscoreFromFriendCode(friend_code: str):
    print(friend_code)



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

def verification(creds: HTTPBasicCredentials = Depends(security)):
    username = creds.username
    password = creds.password
    user = manager.verifyUser(username, password)
    if user is not None:
        print("User validated")
        return True
    else: 
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"}
        )

# end point for login verification
@app.post("/auth")
async def search(Verification = Depends(verification)):
    if Verification:
        # replace this with what we actually want to do
        return {"Hello"}

# get username from email
@app.get("/search/username-from-email/{email}")
async def searchUserFromEmail(email: str):
    ret = manager.userBase.getUserByEmail(email)
    if ret:
        return {ret}
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="could not find username from email",
            headers={"WWW-Authenticate": "Basic"}
        )