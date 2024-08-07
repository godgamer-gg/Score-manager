import json
import sys
import jsonpickle
from .handlers.steamHandler import SteamHandler
from .handlers.riotHandler import RiotHandler
from .handlers.xboxHandler import XboxHandler
from .utils import User, Handler, ScoreCalculator

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
    users = dict()

    def __init__(self):
        # load every score from local database
        try: 
            with open(self.json_file, 'r') as file:
                self.users = json.load(file)
                print(type(self.users))
        except json.decoder.JSONDecodeError:
            # File was empty
            pass 

        # initialize each handler
        self.platformHandlers = dict()
        for platform in PLATFORM_HANDLERS.keys():
           self.platformHandlers[platform] = self.makeHandler(handler_class=PLATFORM_HANDLERS[platform])

    def shutdown(self):
        self.storeUsers()

    def makeHandler(self, handler_class: Handler) -> Handler:
       return handler_class()

    def storeUsers(self):
        print("storing user info")
        with open(self.json_file, "w") as file:
            print(self.users)
            json_out = jsonpickle.encode(self.users)
            json.dump(json_out, file)
            # file.write(self.userScores)

    def loadUser(self, userID: str):
        return self.users[userID]

    # update score for every user to match the newest version
    # This will fail on some users that change privacy on accounts, delete them, or whatever
    # need to handle that case
    def updateAllScores(self):
        for user in self.users:
            if user.lastScoreVersion is not VERSION:
                self.calculateScoreForUser(user, store=False)
        self.storeUsers()
    
    def addUser(self, user: User):
        print("adding user: ", user.userID)
        self.users[user.userID] = user
              
    # calculate all steam scores for a user, usually for a guest user
    def calculateSteamScores(self, userID):
        results = self.platformHandlers["steam"].getScores()
        print(results)
        # probably return total and some stats 
        totalScore = 0
        for entry in results:
            name, val = entry
            totalScore += val
        return totalScore

    # calculates and updates the score for a given user
    # pass update=True if you would like to recalc the score even if the version is the same
    # for more efficient coding please call store=False for repeated calls and then manually call store users for now
    def calculateScoresForUser(self, user: User, update=False, store=True):
        if user.userID not in self.users.keys():
            self.addUser(user)
        # iterate through all of the platforms registered for the user and get scores
        # this doesn't check if a user has an account for other platforms
        if update and user.lastScoreVersion is VERSION:
            return
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

        if store:
            self.storeUsers()

             
            
             
       
              