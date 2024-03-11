import json    
from uuid import uuid4
from ScoreManager import ScoreCalculator

# Global constants
COMP_MAX_SCORE = 300000 # Maximum value each comp game can produce for getting to the max rank

ACHIEV_MAX_SCORE = 100000

# tossing stuff in here that doesn't have a permanent home

def pprint(data):
        json_str = json.dumps(data, indent=4)
        print(json_str)
    
def initCalculator(self, calculator: type[ScoreCalculator]) -> ScoreCalculator:
     return calculator()

# perhaps converting this to a struct would be more efficient
# just using this to make packaging information easier
class User:
    userID = None
    lastScore = None
    lastScoreBreakdown = None
    lastScoreVersion = None
    # platform name: info needed to access account
    accounts = dict[str: list[str]]
    platforms = list[str]

    def __init__(self, steamCode=None, email=None, discord=None, platforms=None):
        self.accounts["steam"] = email
        self.accounts["email"] = email
        self.accounts["discord"] = discord
        self.platforms = platforms
        self.userID = str(uuid4())
          



