import json
import jsonpickle
from scoring.scoreManager import ScoreManager
from utils import User

JSON_FILE = "database.json"

# Entry point for the backend server to call into the actual operations of the system
class Manager():

    def __init__(self):
        # load every score from local database
        self.userBase = UserBase()
        self.scoreManager = ScoreManager(self.userBase)

    # creates a new user
    def create_account(self, username, password):
        act = User(username, password)
        self.store_user(act)

    # returns a given user based on userID
    # def load_user(self, userID):
            
# Handles the storing and loading of users 
class UserBase():

    def __init__(self):
        self.users = dict()
        self.json_file = JSON_FILE
        try: 
            with open(self.json_file, 'r') as file:
                json_obj = json.load(file)
                self.users = jsonpickle.decode(json_obj)
            print("successfully loaded users")
        except json.decoder.JSONDecodeError:
            # File was empty
            print("JSON DECODER ERROR IN USER BASE")
            pass 
        
    def get_user(self, userID: str) -> User:
        if userID in self.users:
            return self.users[userID]
        return None
    
    # could change this to a generic implementation by any field
    def get_user_by_email(self, email: str) -> User:
        for user in self.users:
            if user.email is email:
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
        self.store_all()
        pass





    


