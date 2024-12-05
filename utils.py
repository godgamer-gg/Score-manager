import json
import string
import random
from uuid import uuid4

# from typing import List, Dict, Tuple

# Global constants
COMP_MAX_SCORE = (
    300000  # Maximum value each comp game can produce for getting to the max rank
)

ACHIEV_MAX_SCORE = 100000

# tossing stuff in here that doesn't have a permanent home

STEAM_SCORES = ["achievement", "DOTA", "RocketLeague", "CSGO"]

POSSIBLE_SCORES = {"Steam": STEAM_SCORES, "Total": ["Total"]}

# just a list version of possible scores
CATEGORIES = ["Total"] + STEAM_SCORES

# --------------------------CLASSES--------------------------------------


# perhaps converting this to a struct would be more efficient
# just using this to make packaging information easier
class User(object):

    # account info
    username: str
    hashed_password: str
    email: str
    token: str
    priviliged: bool
    guest: bool
    # cosmetic
    # flairs: list[str] Later on

    userID: str
    # lastScoreBreakdown
    last_score_version: str
    # platform name: info needed to access account

    def __init__(self, username=None, password=""):
        if username == None:
            self.username = "".join(random.choices(string.ascii_letters, k=14))
        else:
            self.username = username
        self.password = password
        if username == "Guest" and password == "Guest":
            self.guest = True
        self.userID = str(uuid4())
        self.scores = {}  # Dict[str: : float]
        self.accounts = {"steam": "", "discord": ""}  # Dict[str: List[str]]
        self.platforms = []  # List[str] = [] # not using platforms anymore
        self.bio = ""

    def preferred_name(self) -> str:
        if hasattr(self, "nickname"):  # this feels jank there must be a better way
            return self.nickname
        else:
            return self.username

    # currently unused, probably deleting soon
    def init_account(
        self,
        guest=False,
        steamCode="",
        discord="",
        platforms=None,
        nickname=None,
    ):
        self.accounts["steam"] = steamCode
        self.accounts["discord"] = discord
        if platforms:
            self.platforms.extend(platforms)
        if not nickname:
            nickname = self.userID
        if steamCode and "steam" not in self.platforms:
            self.platforms.append("steam")


# base class for any handler
class Handler:

    def __init__(self):
        pass

    # get the scores for all of the games a user has on a platform
    def get_scores(
        self, user: User
    ):  # -> List[Tuple[str, float]]: python hates this and I don't want to figure it out right now
        return []

    # confirm if a user has an account on a platform
    def check_user(self, user: User) -> bool:
        return False


# Use this as a base class for any new calculator
class ScoreCalculator:
    name: str

    def __init__(self):
        pass

    def calculate_score(self, user):
        pass


# -----------------------------------FUNCTIONS-------------------------------------


def pprint(data):
    json_str = json.dumps(data, indent=4)
    print(json_str)


def init_calculator(calculator: ScoreCalculator) -> ScoreCalculator:
    return calculator()
