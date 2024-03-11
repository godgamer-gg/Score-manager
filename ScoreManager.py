import json
from handlers.steamHandler import SteamHandler
from handlers.riotHandler import RiotHandler
from handlers.xboxHandler import XboxHandler
from utils import User

VERSION = 0.04

# One of these need to be made for each API we get scores from
# These will call the individual calculator for each game
# if t
PLATFORM_HANDLERS = {
   "steam": SteamHandler,
   "xbox": XboxHandler,
   "riot": RiotHandler
}

# base class for any handler
class Handler():
   
    # get the scores for all of the games a user has on a platform
    def getScores(self, user: User) -> list[(str, float)]:
        return []
    
    # confirm if a user has an account on a platform
    def checkUser(self, user: User) -> bool:
        return False

# Use this as a base class for any new calculator
class ScoreCalculator():
    
    def calculateScore(self, user):
        pass

# High level function calls - ideally server calls from here
# Right now the score manager's job is to call the handlers for each game, which
# will then get the users games on that platform
# currently the handler returns the list of scores, but it could make sense to instead
# have them do just the achievemnt score and then return the list of games to be calculated
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
              
    def calculateScoresForUser(self, user: User):
        # iterate through all of the platforms registered for the user and get scores
        # this doesn't check if a user has an account for other platforms
        allScores = {}
        for platform in user.platforms:
            scores = Handler(self.platformHandlers[platform]).getScores(user)
            # if they game is already contained, use the max
            for entry in scores:
                name, val = entry
                if name in allScores:
                    allScores[name] = max(allScores[name], val)

        totalScore = 0
        for score in allScores:
            totalScore += score

        # need to subdivide scores by game type at some point
        user.lastScoreBreakdown = allScores
        user.lastScore = totalScore
        user.lastScoreVersion = VERSION

             
            
             
       
              