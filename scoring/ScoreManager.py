import json
import sys
import jsonpickle
from .handlers.steamHandler import SteamHandler
from .handlers.riotHandler import RiotHandler
from .handlers.xboxHandler import XboxHandler
from utils import User, Handler, ScoreCalculator

# VSCODE BROKE SPACES AND TABS I KNOW IT'S TERRIBLE RIGHT NOW I WILL SLOWLY BE FIXING


VERSION = 0.04

# One of these need to be made for each API we get scores from
# These will call the individual calculator for each game
# if t
PLATFORM_HANDLERS = {
   "steam": SteamHandler,
   "xbox": XboxHandler,
   "riot": RiotHandler
}

# High level function calls - ideally server calls from here
# Right now the score manager's job is to call the handlers for each game, which
# will then get the users games on that platform
# currently the handler returns the list of scores, but it could make sense to instead
# have them do just the achievemnt score and then return the list of games to be calculated
class ScoreManager():
    json_file = "userInfo.json"

    def __init__(self, userBase):

        self.userBase = userBase
        # initialize each handler
        self.platformHandlers = dict()
        for platform in PLATFORM_HANDLERS.keys():
           self.platformHandlers[platform] = self.makeHandler(handler_class=PLATFORM_HANDLERS[platform])

    # in case any changes were missed store all changes
    def shutdown(self):
        self.userBase.storeAll()

    def makeHandler(self, handler_class: Handler) -> Handler:
       return handler_class()

    # update score for every user to match the newest version
    # This will fail on some users that change privacy on accounts, delete them, or whatever
    # need to handle that case
    def updateAllScores(self):
        for user in self.users:
            if user.lastScoreVersion is not VERSION:
                self.calculateScoreForUser(user, store=False)
            # self.userBase.update_user(user)
        self.userBase.store_all()
              
    # calculate all steam scores for a guest user
    def calculateSteamScoresForGuest(self, steamCode: str):
        guestUser = User(guest=True, steamCode=steamCode)
        results = self.platformHandlers["steam"].getScores(guestUser)
        print(results)
        # probably return total and some stats 
        totalScore = 0
        for entry in results:
            name, val = entry
            if val is not None:
                totalScore += val   
        return totalScore

    # TODO: combine this and above function for cleaner code
    # calculate all steam scores for a given user
    def calculateSteamScoresForUser(self, user: User):
        results = self.platformHandlers["steam"].getScores(user)
        print(results)
        # probably return total and some stats 
        totalScore = 0
        for entry in results:
            name, val = entry
            if val is not None:
                totalScore += val  
        user.scores["steam"] = results
        user.lastScoreVersion = VERSION
        self.userBase.update_user(user)
        return totalScore
    
    # calculates and updates the score for a given user
    def calculateScoresForUser(self, user: User):
        # Assuming user has already been added by the current workflow
        # if user.userID not in self.users.keys():
        #     self.addUser(user)
        # iterate through all of the platforms registered for the user and get scores
        # this doesn't check if a user has an account for other platforms
        allScores = {}
        for platform in user.platforms:
            print("calculating score for platform: ", platform)
            scores = self.platformHandlers[platform].getScores(user)
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
        self.userBase.update_user(user)

             
            
             
       
              