import jsonpickle
from utils import User, CATEGORIES
from pprint import pprint

from userBase import UserBase

# Remove the relative import attempt and just use the absolute import
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scoring.scoreManager import ScoreManager

# settings to make sure jsonpickle will properly function
jsonpickle.set_encoder_options("json", sort_keys=True)
jsonpickle.register(User)
# Force jsonpickle to fully encode custom objects and dictionaries
jsonpickle.set_encoder_options("json", unpicklable=True)


# Entry point for the backend server to call into the actual operations of the system
class Manager:

    def __init__(self):
        print("creating manager")
        # load every score from local database
        self.user_base = UserBase()
        self.score_manager = ScoreManager(self.user_base)

    # creates a new user
    def create_account(self, username, password, email=None) -> User:
        act = User(username, password)
        if email is not None:
            act.email = email
        self.user_base.add_user(act)
        return act

    # if a username and password matches returns the user, otherwise returns None
    def verify_user(self, username, password) -> User:
        result = self.user_base.get_user_by_username(username)
        # better to throw an error here and handle it
        if result is None:
            raise ValueError("username not found")
        if result.password != password:
            raise ValueError("incorrect password")
        return result

    # calculates all scores for guest
    def calculate_guest_scores(self, platforms):
        guestUser = User()
        guestUser.guest = True

    # recalculates all scores for a user, returns the users scores along with percentiles and rank
    def calculate_user_scores(self, username: str):
        user = self.user_base.get_user_by_username(username)

        if not hasattr(
            user, "scores"
        ):  # solve a bug where sometimes scores isn't instantiated
            user.scores = {}
        # update users scores
        self.score_manager.calculate_scores_for_user(user)

        return self.get_user_score_breakdown(user=user)

    # gets users scores, percentile, and grades based on either username or user
    def get_user_score_breakdown(self, username=None, user=None):
        if user is None:
            if username is None:
                return
            user = self.user_base.get_user_by_username(username)
        stats = self.score_manager.get_user_score_stats(user)
        print("score stats: ", stats)

        ret = {}

        for cat in user.scores:
            print(user.scores[cat])
            ret[cat] = [user.scores[cat]] + stats[cat]

        return ret

    # gets a list of all available categories
    def get_leaderboard_categories(self):
        return CATEGORIES

    # get all the scores for a given category, converts from entry
    def get_leaderboard_data(self, cat):
        if cat in self.score_manager.scores_db:
            ret = []
            for entry in self.score_manager.scores_db[cat]:
                ret.insert(0, entry.format())
            return ret
        else:
            return ValueError
