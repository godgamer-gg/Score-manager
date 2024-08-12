import json    
from uuid import uuid4
# from typing import List, Dict, Tuple

# Global constants
COMP_MAX_SCORE = 300000 # Maximum value each comp game can produce for getting to the max rank

ACHIEV_MAX_SCORE = 100000

# tossing stuff in here that doesn't have a permanent home



# --------------------------CLASSES--------------------------------------

# perhaps converting this to a struct would be more efficient
# just using this to make packaging information easier
class User:

	# account info
	username: str
	password: str
	token: str
	priviliged: bool

	guest: bool

	# cosmetic 
	nickname: str
	# flairs: list[str] Later on
	
	userID: str
	lastScore: float
	# lastScoreBreakdown
	lastScoreVersion: str
    # platform name: info needed to access account
	accounts = {} # Dict[str: List[str]]
	platforms = [] # List[str] = []

	def __init__(self, username, password, ):
		self.username = username
		self.password = password
		self.userID = str(uuid4())

	def init_account(self, guest=False, steamCode=None, email=None, discord=None, platforms=None, nickname=None):
		self.accounts["steam"] = steamCode
		self.accounts["email"] = email
		self.accounts["discord"] = discord
		if platforms:
			self.platforms.extend(platforms)
		if not nickname:
			nickname = self.userID
		if steamCode and "steam" not in self.platforms:
			self.platforms.append("steam")

# base class for any handler
class Handler():
    
	def __init__(self):
		pass
   
# get the scores for all of the games a user has on a platform
	def getScores(self, user: User): # -> List[Tuple[str, float]]: python hates this and I don't want to figure it out right now
		return []
    
# confirm if a user has an account on a platform
	def checkUser(self, user: User) -> bool:
		return False

# Use this as a base class for any new calculator
class ScoreCalculator():
	name: str

	def __init__(self):
		pass
    
	def calculateScore(self, user):
		pass
          

# -----------------------------------FUNCTIONS-------------------------------------

def pprint(data):
	json_str = json.dumps(data, indent=4)
	print(json_str)
    
def initCalculator(calculator: ScoreCalculator) -> ScoreCalculator:
	return calculator()


