import json
from handlers.steamHandler import SteamHandler
from utils import User

VERSION = 0.04

# One of these need to be made for each API we get scores from
# These will call the individual calculator for each game
# if t
PLATFORM_HANDLERS = {
   "steam": SteamHandler
}

# base class for any handler
class Handler():
   
   def getScores(self, user: User) -> list[(str, float)]:
      pass

# Use this as a base class for any new calculator
class ScoreCalculator():
    
    def calculateScore(self, user):
        pass

# High level function calls - ideally server calls from here

class ScoreManager():
    json_file = "userInfo.json"

    def __init__(self):
        # load every score from local database
        with open(self.json_file, 'r') as file:
           self.userScores = json.load(file)

        # initialize each handler
        self.platformHandlers = dict()
        for platform in PLATFORM_HANDLERS.keys():
           self.platformHandlers[platform] = self.makeHandler(PLATFORM_HANDLERS[platform])
           
        
    def makeHandler(self, handler_class: type[Handler]) -> Handler:
       return handler_class()

    def storeUsers(self):
      with open(self.json_file, "w") as file:
         json.dump(self.userScores, file)

    def loadUser(self, userID: str):
      return self.userScores[userID]

    # update score for every user to match the newest version
    def updateAllScores(self):
        for user in self.userScores:
           if user.lastScoreVersion is not VERSION:
              self.calculateScoreForUser(user)
              
    def calculateScoreForUser(self, user: User):
        # iterate through all of the platforms registered for the user
       allScores = []
       for platform in user.platforms:
          scores = Handler(self.platformHandlers[platform]).getScores(user)
            
             
       
              