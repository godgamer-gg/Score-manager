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


origins = ["http://localhost", "http://localhost:8000", "http://localhost:3000"]

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


# ------------AUTHORIZATION----------------------------------
def verification(creds: HTTPBasicCredentials = Depends(security)):
    username = creds.username
    password = creds.password
    try:
        user = manager.verify_user(username, password)
        if user is not None:
            print("User validated")
            return True
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error.args[0],
            headers={"WWW-Authenticate": "Basic"},
        )


# end point for login verification
@app.post("/auth")
async def login(
    Verification=Depends(verification), creds: HTTPBasicCredentials = Depends(security)
):
    if Verification:
        nickname = manager.user_base.get_user_by_username(
            creds.username
        ).preferred_name()
        token = jwt.encode({"sub": nickname}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}


# authenticate an existing toker for a user
@app.post("/auth/verify")
async def verify_token(authorization: str = Header(...)):
    token = authorization.split(" ")[1]  # Extract Bearer token
    try:
        data = jwt.decode(key=SECRET_KEY, token=token, algorithms=[ALGORITHM])
        username = data.get("sub")
        if not username:
            print("token validation failed for data: ", data)
            raise HTTPException(status_code=401, detail="Token validation failed")
        return {"username": username}
    except Exception as e:
        print("error validating token: ", e, "with token: ", token)
        raise HTTPException(
            status_code=401, detail="Error validating token {e.args[0]}"
        )


# advanced verifiation that also returns all of the users info
# currently returns: username, email, steamID, discord, bio
@app.post("/auth/current-user")
async def verify_and_return_current_user(payload: dict = Depends(verify_token)):
    username = payload["username"]
    print("detailed session request received for: ", username)
    user = manager.user_base.get_user_by_username(username)
    if hasattr(user, "accounts"):
        print("accounts: ", user.accounts)
        discord = user.accounts["discord"] if "discord" in user.accounts else ""
        steam = user.accounts["steam"] if "steam" in user.accounts else ""
    else:
        # bug where sometimes accounts dict is not created
        user.accounts = {"discord": "", "steam:": ""}
        discord = ""
        steam = ""

    return {
        "username": username,
        "email": user.email,
        "discord": discord,
        "steam": steam,
        "bio": user.bio,
    }


# --------------------BASICS---------------------------------


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hello")
def say_hello():
    return {"Hello!"}


# ------------------------------SCORING----------------------------------
# fetches users current scores, does not calculate them
@app.get("/scoring/all/user/current")
async def get_all_users_scores(payload: dict = Depends(verify_token)):
    username = payload["username"]
    return manager.get_user_score_breakdown(username=username)


# calculates users scores, percentiles, grade and then returns them
@app.get("/scoring/all/user/update")
async def calculate_all_users_scores(payload: dict = Depends(verify_token)):
    username = payload["username"]
    print("Full score request received for: ", username)

    try:
        ret = manager.calculate_user_scores(username)
        print("finished calculating scores for user: ", ret)
        return ret
    except ValueError as e:
        print("Value error calculating scores")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.args[0],
            headers={"WWW-Authenticate": "Basic"},
        )
    except Exception as e:
        print("exception calculating scores: ", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="internal server error",
            headers={"WWW-Authenticate": "Basic"},
        )


# calculates score based on steamcode
@app.get("/scoring/steam/user")
async def get_steamscore_from_ID(payload: dict = Depends(verify_token)):
    username = payload["username"]
    print("Steam score request received for: ", username)
    user = manager.user_base.get_user_by_username(username)
    score = manager.score_manager.calculate_user_steam_scores(user)
    # We'll want to return a more in depth breakdown later
    return {score}


# calculates steam score for a guest based on their steamcode
# currently no way to validate that code is actually theirs
@app.get("/scoring/steam/guest")
async def get_guest_steamscore(steam_id: str):
    print(steam_id)
    score = manager.score_manager.calculate_guest_steam_scores(steam_id)
    return {score}


# I thought there was a way to get steamcode from friend code
# but I think you can only do the reverse
# @app.get("/steamscore/friendCode/{friend_code}")
# async def get_steamscore_from_friendcode(friend_code: str):
#     print(friend_code)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# -----------------------------------ACCOUNTS--------------------------------------


# get username from email
@app.get("/search/username-from-email")
async def search_user_from_email(email: str):
    ret = manager.user_base.get_user_by_email(email)
    if ret:
        return {ret}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="could not find username from email",
            headers={"WWW-Authenticate": "Basic"},
        )


class NewAccount(BaseModel):
    username: str
    email: str
    password: str


@app.post("/register")
async def create_account(act: NewAccount):
    try:
        user = manager.create_account(act.username, act.password, act.email)
        print("account created: ", user)
        token = jwt.encode({"sub": act.username}, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error.args[0])


class AccountUpdateInfo(BaseModel):
    username: str
    email: str
    steam_id: str
    discord: str
    bio: str


@app.post("/profile/update")
async def update_user_profile(
    act_info: AccountUpdateInfo, payload: dict = Depends(verify_token)
):
    username = payload["username"]
    print("updating userinfo for: ", username)
    print("account info received: ", act_info)
    user = manager.user_base.get_user_by_username(username)
    user.username = act_info.username
    if not hasattr(user, "accounts"):
        user.accounts = {}
    user.accounts["steam"] = act_info.steam_id
    user.accounts["email"] = act_info.email
    user.accounts["discord"] = act_info.discord
    user.bio = act_info.bio
    manager.user_base.update_user(user)
