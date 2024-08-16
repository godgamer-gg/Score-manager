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
        if self.userBase.contains_uesrname(username):
            raise ValueError("username already exists")
        act = User(username, password)
        self.userBase.addUser(act)

    # if a username and password matches returns the user, otherwise returns None
    def verifyUser(self, username, password) -> User:
        result = self.userBase.getUserByUsername(username)
        # better to throw an error here and handle it
        if result is None:
            print("user not found")
            return None
        if result.password != password:
            print("passwords did not match")
            print(result.password, password)
            return None
        return result

            
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
        
    def getUser(self, userID: str) -> User:
        if userID in self.users:
            return self.users[userID]
        return None
    
    # could change this to a generic implementation by any field
    def getUserByEmail(self, email: str) -> User:
        for id in self.users:
            user = self.users[id]
            if user.email is not None and user.email is email:
                return user
        return None
    
    def getUserByUsername(self, username: str) -> User:
        for id in self.users:
            user = self.users[id]
            if user.username is not None and user.username == username:
                return user 
        return None

    def getAllUsers(self):
        return self.users
    
    # stores all users in the json file, call this when updating info for a user
    def storeAll(self):
        print("storing all")
        with open(self.json_file, "w") as file:
            json_obj = jsonpickle.encode(self.users)
            json.dump(json_obj, file)
    
    # adds a user then stores the updated json object
    def addUser(self, act: User):
        print("storing user: ", act.userID)
        self.users[act.userID] = act
        self.storeAll()

    # since python is pass by reference this function isn't quite as necessary but will
    # just call store all for now
    def updateUser(self, act: User):
        self.storeAll()
        pass


        
        
        




    


