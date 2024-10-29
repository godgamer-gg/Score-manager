import json
import sys
import jsonpickle
import bisect
from .handlers.steamHandler import SteamHandler
from .handlers.riotHandler import RiotHandler
from .handlers.xboxHandler import XboxHandler
from utils import User, Handler, ScoreCalculator, POSSIBLE_SCORES

# VSCODE BROKE SPACES AND TABS I KNOW IT'S TERRIBLE RIGHT NOW I WILL SLOWLY BE FIXING


VERSION = 0.04

# One of these need to be made for each API we get scores from
# These will call the individual calculator for each game
PLATFORM_HANDLERS = {"steam": SteamHandler, "xbox": XboxHandler, "riot": RiotHandler}


# High level function calls - ideally server calls from here
# Right now the score manager's job is to call the handlers for each game, which
# will then get the users games on that platform
# currently the handler returns the list of scores, but it could make sense to instead
# have them do just the achievemnt score and then return the list of games to be calculated
class ScoreManager:
    json_file = "userInfo.json"

    def __init__(self, user_base):

        self.user_base = user_base
        # initialize each handler
        self.platform_handlers = dict()
        for platform in PLATFORM_HANDLERS.keys():
            self.platform_handlers[platform] = self.make_handler(
                handler_class=PLATFORM_HANDLERS[platform]
            )

        # build scores dict
        self.scores_db = dict()  # string (score type) -> [*->float] should be sorted
        for lis in POSSIBLE_SCORES.values():
            for cat in lis:
                self.scores_db[cat] = []
        for user in self.user_base.get_all_users():
            if hasattr(user, "scores"):  # in case user hasn't logged any scores yet
                for platform in user.scores:
                    for cat in platform:
                        self.scores_db[cat].append(user.scores[platform][cat])
        print(self.scores_db)

    # in case any changes were missed store all changes
    def shutdown(self):
        self.user_base.storeAll()

    def make_handler(self, handler_class: Handler) -> Handler:
        return handler_class()

    # update score for every user to match the newest version
    # This will fail on some users that change privacy on accounts, delete them, or whatever
    # need to handle that case
    def update_all_scores(self):
        for user in self.users:
            if user.last_score_version is not VERSION:
                self.calculate_score_for_user(user, store=False)
            # self.user_base.update_user(user)
        self.sort_scoresDB()
        self.user_base.store_all()

    # ensure all values of scores database are sorted
    def sort_scoresDB(self):
        print("TODO SORTING SCORES DB")

    # calculate all steam scores for a guest user
    def calculate_guest_steam_scores(self, steam_code: str):
        # TODO: probably should make it so you can't enter a steam code for an existing user
        guestUser = User()
        guestUser.accounts["steam"] = steam_code
        results = self.platform_handlers["steam"].get_scores(guestUser)
        print(results)
        # probably return total and some stats
        total_score = 0
        for entry in results:
            name, val = entry
            if val is not None:
                total_score += val

        # TODO: need to also update db logic to store guest scores
        bisect.insort(self.scores_db["steam_achievement"], total_score)
        return total_score

    # calculate all steam scores for a given user
    def calculate_user_steam_scores(self, user: User):
        results = self.platform_handlers["steam"].getScores(user)
        print(results)
        # probably return total and some stats
        totalScore = 0
        for entry in results:
            name, val = entry
            if val is not None:
                totalScore += val
        user.scores["steam"] = results
        user.last_score_version = VERSION
        self.user_base.update_user(user)
        return totalScore

    # calculates and updates the score for a given user
    def calculate_scores_for_user(self, user: User):
        # Assuming user has already been added by the current workflow
        # if user.userID not in self.users.keys():
        #     self.addUser(user)
        # iterate through all of the platforms registered for the user and get scores
        # this doesn't check if a user has an account for other platforms
        allScores = {}
        for platform in user.platforms:
            print("calculating score for platform: ", platform)
            scores = self.platform_handlers[platform].getScores(user)
            # if they game is already contained, use the max
            for entry in scores:
                name, val = entry
                if name in allScores:
                    allScores[name] = max(allScores[name], val)

        totalScore = 0
        for score in allScores:
            totalScore += score

        # need to subdivide scores by game type at some point
        user.last_score_breakdown = allScores
        user.last_score = totalScore
        user.last_score_version = VERSION
        self.user_base.update_user(user)
