# TO RUN THIS FILE python3 -m uvicorn runServer:app --reload


# import sys
# from pathlib import Path
import logging
import os

from typing import Union
from fastapi import FastAPI, Header, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, find_dotenv
from jose import jwt, JWTError
# from typing import Optional
# from datetime import datetime, timedelta

from manager import Manager

load_dotenv(find_dotenv())
# Fetch the secret key from environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if SECRET_KEY is None:
    raise ValueError("Secret key not found in environment variables")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define OAuth2 and HTTPBasic security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBasic()
app = FastAPI()
# app = FastAPI(dependencies=[Depends(security)]) # this will require http basic on every request which is bad


logging.basicConfig(level=logging.INFO)

manager = Manager()


# # init scoremanager on startup
# # post refactoring this is probably no longer necessary, leaving in case it's needed
# async def lifespan(app: FastAPI):
#     logger = logging.getLogger("uvicorn.info")
#     logger.info('scoreManager init')
#     yield
#     manager.scoreManager.shutdown()
#     logger.info("Shut down scoremanager")
# app = FastAPI(lifespan=lifespan, dependencies=[Depends(security)]) -> to use lifespan



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

# calculates score based on steamcode
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
    try: 
        user = manager.verifyUser(username, password)
        if user is not None:
            print("User validated")
            return True
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=error.args[0],
            headers={"WWW-Authenticate": "Basic"}
        )

# end point for login verification
@app.post("/auth")
async def login(Verification = Depends(verification), creds: HTTPBasicCredentials = Depends(security)):
    if Verification:
        nickname = manager.userBase.getUserByUsername(creds.username).preferred_name()
        token = jwt.encode({"sub": nickname}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    
# authenticate an existing toker for a user
@app.post("/auth/verify")
async def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]  # Extract Bearer token
    print("token: ", token)
    print("here")
    try:
        print("here")
        data = jwt.decode(key=SECRET_KEY, token=token, algorithms=[ALGORITHM])
        print("data: ", data)
        username = data.get("sub")
        print("username: ", username)
        if not username:
            raise HTTPException(status_code=401, detail="Token validation failed")
        return {"username": username}
    except Exception as e:
        print("error validating token: ", e)
        raise HTTPException(status_code=401, detail="Error validating token {e}")

# get username from email
@app.get("/search/username-from-email")
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

class NewAccount(BaseModel):
    username: str
    email: str
    password: str

@app.post("/register")
async def create_account(act: NewAccount):
    try:
        user = manager.create_account(act.username, act.password, act.email)
        return {"account created: ", user}
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.args[0])
        
