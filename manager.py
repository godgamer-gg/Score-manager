import json
from scoring.scoreManager import ScoreManager
from .utils import User

JSON_FILE = "database.json"

# Entry point for the backend server to call into the actual operations of the system
class Manager():

    def __init__(self):
        # load every score from local database
        self.users = dict()
        try: 
            with open(JSON_FILE, 'r') as file:
                self.users = json.load(file)
                print(type(self.users))
        except json.decoder.JSONDecodeError:
            # File was empty
            pass 
            
        self.scoreManager = ScoreManager(self.users)

    def create_account(self, username, password):
        act = User(username, password)
        
