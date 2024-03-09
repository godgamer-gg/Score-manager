import json    
from uuid import uuid4

# tossing stuff in here that doesn't have a permanent home

def pprint(data):
        json_str = json.dumps(data, indent=4)
        print(json_str)

# perhaps converting this to a struct would be more efficient
# just using this to make packaging information easier
class User:
    userID = None
    steamCode = None
    email = None
    lastScore = None
    lastScoreVersion = None

    def __init__(self, steamCode=None, email=None):
        self.steamCode = steamCode
        self.email = email
        self.userID = str(uuid4())
          



