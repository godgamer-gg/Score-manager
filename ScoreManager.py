import json
from steamScoreCalculators import SteamAchievementScoreCalculator
from utils import User


CALCULATORS = [
    SteamAchievementScoreCalculator,
]

VERSION = 0.04

# Use this as a base class for any new calculator
class ScoreCalculator():
    
    def calculateScore():
        pass

# High level function calls - ideally server calls from here

class ScoreManager():
    json_file = "userInfo.json"

    def __init__(self):
        with open(self.json_file, 'r') as file:
           self.userScores = json.load(file)


        # functions to load and store user info
    
    def storeUsers(self):
      with open(self.json_file, "w") as file:
         json.dump(self.userScores, file)

    def loadUser(self, userID: str):
      return self.userScores[userID]

# update score for every user to match the newest version
    def updateAllScores(self):
        for user in self.userScores:
           if user.version is not VERSION:
              