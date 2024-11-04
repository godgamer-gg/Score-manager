import jsonpickle
from scoring.scoreManager import ScoreManager
from utils import User
from pprint import pprint

from userBase import UserBase

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
