import json
import jsonpickle
import string
import datrie

from pprint import pprint
from utils import User

JSON_FILE = "database.json"


# Handles the storing and loading of users
# Helper class to manager, other classes should not directly call into this
class UserBase:
    def __init__(self):
        self.users = dict()  # id -> user
        self.json_file = JSON_FILE
        self.username_lookup = datrie.Trie(string.ascii_lowercase)
        self.load_users()

    def load_users(self):
        try:
            with open(self.json_file, "r") as file:
                json_obj = json.load(file)
                self.users = jsonpickle.decode(json_obj)
            print("successfully loaded users")
        except json.decoder.JSONDecodeError:
            # File was empty
            print("JSON DECODER ERROR IN USER BASE")
            pass
        for user in self.users.values():
            self.username_lookup[user.username.lower()] = user.userID
        print("built username lookup")

    # returns the user based on their userID
    def get_user(self, userID: str) -> User:
        if userID in self.users:
            return self.users[userID]
        return None

    def username_prefix_lookup(self, prefix: str):
        return self.username_lookup.keys(prefix.lower())

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

    # deletes a user if they are within the UserBase
    # perhaps make this more versatile to handle other inputs
    def delete_user(self, UID):
        if UID in self.users:
            del self.users[UID]
        self.store_all()

    # returns a list of all users
    def get_all_users(self):
        return self.users.values()

    # stores all users in the json file, call this when updating info for a user
    def store_all(self):
        print("storing all")
        with open(self.json_file, "w") as file:
            json_obj = jsonpickle.encode(self.users)
            json.dump(json_obj, file)

    # adds a user then stores the updated json object
    def add_user(self, act: User):
        if self.contains_username(act.username):
            print("contains username", act.username)
            raise ValueError("username already exists")
        if hasattr(act, "email") and self.contains_email(act.email):
            raise ValueError("account with this email already exists")
        print("storing user: ", act.userID)
        self.users[act.userID] = act
        self.store_all()

    # since python is pass by reference this function isn't quite as necessary but will
    # just call store all for now
    def update_user(self, act: User):
        print("updating user: ", act.username)
        self.store_all()
        pass

    # -----UTIL FUNCTIONS--------
    def print_all(self):
        for user in self.users.values():
            pprint(vars(user))
            print()

    # runs through the user base to make sure there are no invalid duplicates
    # writing this in 0(n^2) but if it becomes a function used more frequently can be redone
    # deleting multiples of username and email
    def clean(self):
        del_list = []
        for user_a in self.users.values():
            if (
                hasattr(user_a, "guest") and user_a.guest
            ):  # keep guests for now as data points
                continue

            for user_b in self.users.values():
                if user_a.userID == user_b.userID:
                    continue
                if hasattr(user_b, "guest") and user_b.guest:
                    continue
                if user_a.username == user_b.username:
                    print("deleting duplicate username: ", user_a.username)
                    print(user_b.userID)
                    del_list.append(user_b.userID)
                elif hasattr(user_a, "email") and hasattr(user_b, "email"):
                    if user_a.email == user_b.username:
                        print("deleting duplicate email: ", user_a.email)
                        del_list.append(user_b.userID)

        for uid in del_list:
            if uid in self.users:
                del self.users[uid]

        self.store_all()
