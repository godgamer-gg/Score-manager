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
    def __init__(self, username=None, password=""):
        # Generate random username if none provided
        self.username = (
            username
            if username
            else "".join(random.choices(string.ascii_letters, k=14))
        )
        self.password = password
        self.userID = str(uuid4())

        # Account information
        self.hashed_password = ""
        self.email = ""
        self.token = ""
        self.privileged = False
        self.guest = True if (username == "Guest" and password == "Guest") else False

        # User profile data
        self.bio = ""
        self.hidden = []  # List of attributes to hide from public view

        # Platform accounts
        self.accounts = {"steam": "", "discord": "", "email": ""}

        # Score tracking
        self.scores = {}  # Dict[str: float]
        self.last_score_version = ""

    def preferred_name(self) -> str:
        """Returns the user's preferred display name"""
        return getattr(self, "nickname", self.username)

    def hide_attribute(self, attribute_name):
        """Add an attribute to the hidden list"""
        if attribute_name not in self.hidden:
            self.hidden.append(attribute_name)

    def unhide_attribute(self, attribute_name):
        """Remove an attribute from the hidden list"""
        if attribute_name in self.hidden:
            self.hidden.remove(attribute_name)

    def update_account(self, platform, value):
        """Update a platform account value"""
        if platform in self.accounts:
            self.accounts[platform] = value


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
