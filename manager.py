import json
import jsonpickle
from scoring.scoreManager import ScoreManager
from utils import User

JSON_FILE = "database.json"


# Entry point for the backend server to call into the actual operations of the system
class Manager:

    def __init__(self):
        print("creating manager")
        # load every score from local database
        self.user_base = UserBase()
        self.score_manager = ScoreManager(self.user_base)

    # creates a new user
    def create_account(self, username, password, email=None) -> User:
        if self.user_base.contains_username(username):
            print("contains username", username)
            raise ValueError("username already exists")
        act = User(username, password)
        if email is not None:
            if self.user_base.contains_email(email):
                raise ValueError("account with this email already exists")
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


# Handles the storing and loading of users
class UserBase:
    def __init__(self):
        self.users = dict()  # id -> user
        self.json_file = JSON_FILE
        try:
            with open(self.json_file, "r") as file:
                json_obj = json.load(file)
                self.users = jsonpickle.decode(json_obj)
            print("successfully loaded users")
        except json.decoder.JSONDecodeError:
            # File was empty
            print("JSON DECODER ERROR IN USER BASE")
            pass

        # settings to make sure jsonpickle will properly function
        jsonpickle.set_encoder_options("json", sort_keys=True)
        jsonpickle.register(User)

    def get_user(self, userID: str) -> User:
        if userID in self.users:
            return self.users[userID]
        return None

    def contains_email(self, email: str) -> bool:
        return self.get_user_by_email(email) is not None

    # could change this to a generic implementation by any field
    def get_user_by_email(self, email: str) -> User:
        for id in self.users:
            user = self.users[id]
            if user.email is not None and user.email is email:
                print(user)
                print("contains email", email)
                return user
        return None

    def contains_username(self, username: str) -> bool:
        return self.get_user_by_username(username) is not None

    def get_user_by_username(self, username: str) -> User:
        for id in self.users:
            user = self.users[id]
            if hasattr(user, "username") and user.username == username:
                return user
        return None

    def get_user_by_email(self, email: str) -> User:
        for id in self.users:
            user = self.users[id]
            if hasattr(user, "email") and user.email == email:
                return user
        return None

    def get_all_users(self):
        return self.users

    # stores all users in the json file, call this when updating info for a user
    def store_all(self):
        print("storing all")
        with open(self.json_file, "w") as file:
            json_obj = jsonpickle.encode(self.users)
            json.dump(json_obj, file)

    # adds a user then stores the updated json object
    def add_user(self, act: User):
        print("storing user: ", act.userID)
        self.users[act.userID] = act
        self.store_all()

    # since python is pass by reference this function isn't quite as necessary but will
    # just call store all for now
    def update_user(self, act: User):

        # settings to make sure jsonpickle will properly function
        jsonpickle.set_encoder_options("json", sort_keys=True)
        jsonpickle.register(User)
        # Force jsonpickle to fully encode custom objects and dictionaries
        jsonpickle.set_encoder_options("json", unpicklable=True)

        print("updating user: ", act.username)
        # print(jsonpickle.encode(act))
        print("accounts: ", act.accounts)
        self.store_all()
        pass
