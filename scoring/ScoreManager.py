import json
import sys
import jsonpickle
import bisect
from sortedcontainers import SortedList
from .handlers.steamHandler import SteamHandler
from .handlers.riotHandler import RiotHandler
from .handlers.xboxHandler import XboxHandler
from utils import User, Handler, ScoreCalculator, POSSIBLE_SCORES

# VSCODE BROKE SPACES AND TABS I KNOW IT'S TERRIBLE RIGHT NOW I WILL SLOWLY BE FIXING


VERSION = 0.04

# One of these need to be made for each API we get scores from
# These will call the individual calculator for each game
PLATFORM_HANDLERS = {"steam": SteamHandler, "xbox": XboxHandler, "riot": RiotHandler}


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
        for user in self.user_base.get_all_users():
            if hasattr(user, "scores"):  # in case user hasn't logged any scores yet
                for cat in user.scores:
                    if not cat in self.scores_db:
                        self.scores_db[cat] = SortedList()
                    self.scores_db[cat].add(entry(user, cat))
        print("scores db int: ", self.scores_db)

    # in case any changes were missed store all changes
    def shutdown(self):
        self.user_base.store_all()

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

    # calculate all steam scores for a given user
    def calculate_user_steam_scores(self, user: User):
        results = self.platform_handlers["steam"].get_scores(user)
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
        totalScore = 0
        for platform in PLATFORM_HANDLERS:
            print("calculating score for platform: ", platform)
            scores = self.platform_handlers[platform].get_scores(user)
            print("scores calculated: ", scores)
            for entry in scores:
                name, val = entry
                if val is None:
                    val = 0

                # update scores_db, python is pass by reference so I'm unsure why this is necessary but it is
                # if name in user.scores:
                #     try:
                #         sorted_lis = self.scores_db[name]
                #         sorted_lis.remove(user.scores[name])
                #         sorted_lis.add(val)
                #     except ValueError:
                #         print("score wasn't in db, investigate bug")
                # default user scores to 0 if they don't have one, this could end up
                # inflating percentiles but that's ok
                print("entry: ", entry)
                if name not in user.scores:
                    user.scores[name] = val
                    self.scores_db[name].add(entry(user, name))
                else:
                    user.scores[name] = val
                totalScore += val

        # overwrite missed scores to 0 as a safety check
        for platform in POSSIBLE_SCORES:
            for cat in POSSIBLE_SCORES[platform]:
                if cat not in user.scores or user.scores[cat] is None:
                    user.scores[cat] = 0

        # need to subdivide scores by game type at some point
        added = "Total" in user.scores
        user.scores["Total"] = totalScore
        if not added:
            self.scores_db["Total"].add(entry(user, "Total"))
        user.last_score_version = VERSION
        print("finished calculating {user.username}'s scores: ", user.scores)
        self.user_base.update_user(user)

    # calculates and returns the percentile (and rank) of a user in all of their score
    # categories. Not a true percentile, returns % of users greater than
    # returns dict[Tuple(float, str)]
    def get_user_score_stats(self, user: User):
        if not hasattr(user, "scores"):
            user.scores = {}
            return {}
        summary = {}
        for entry in user.scores:
            lis = self.scores_db[entry]
            score = user.scores[entry]
            print("entry: ", entry)
            print("list: ", lis)
            print("score: ", score)
            if lis is None or len(lis) is None or score is None:
                continue
            try:
                # pos = self.scores_db[entry].index(user.scores[entry])
                pos = lis.index(score)
                if pos is 0:
                    percentile = 0
                else:
                    size = len(self.scores_db[entry])
                    print("size:", size, "pos:", pos)
                    percentile = 1 - ((size - pos - 1) / size)
                    print("percentile: ", percentile)
                summary[entry] = [percentile, self.grade(percentile)]
            except ValueError:
                print("score wasn't saved in db")
                summary[entry] = [0, "N/A"]
        return summary

    # probably should make these more lenient so 40% of people don't have an S
    grade_percents = {
        0.99: "SS+",
        0.97: "SS",
        0.95: "S+",
        0.90: "S",
        0.85: "A+",
        0.80: "A",
        0.75: "A-",
        0.70: "B+",
        0.65: "B",
        0.60: "C+",
        0.55: "C",
        0.5: "D+",
        0.45: "D",
        0.40: "D-",
        0.30: "E",
    }

    def grade(self, percentile: float) -> str:
        if percentile is None or percentile is 0:
            return "N/A"
        for val in self.grade_percents:
            if percentile > val:
                return self.grade_percents[val]
        return "F"


# -------------------------------HELPERS---------------------------------------


# just a container class for entries into the scores_db that is comparable
class entry:
    def __init__(self, user, key):
        self.user = user
        self.key = key

    def value(self):
        return self.user.scores[self.key]

    def __lt__(self, other):
        if isinstance(other, entry):
            return self.value() < other.value()
        return NotImplementedError

    def __le__(self, other):
        if isinstance(other, entry):
            return self.value() <= other.value()
        return NotImplementedError

    def __eq__(self, other):
        if isinstance(other, entry):
            return self.value() == other.value()
        return NotImplementedError

    def __ne__(self, other):
        if isinstance(other, entry):
            return self.value() != other.value()
        return NotImplementedError

    def __gt__(self, other):
        if isinstance(other, entry):
            return self.value() > other.value()
        return NotImplementedError

    def __ge__(self, other):
        if isinstance(other, entry):
            return self.value() >= other.value()
        return NotImplementedError

    def __str__(self):
        return "(" + str(self.value()) + ", " + self.user.username + ")"

    def __repr__(self) -> str:
        return self.__str__()

    def format(self) -> str:
        return [str(self.value()), self.user.username]
