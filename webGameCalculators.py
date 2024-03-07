import requests
from utils import pprint

class TETRIOCalculator():

    def __init__(self):
        self.baseEndpoint = "https://ch.tetri.io/api/"

    def calculateScore(self, username):
        self.getUserInfo(username)

    def getUserNameFromDiscord(self, discord) -> str:
        response = requests.get(self.baseEndpoint + "users/search/discord" + discord)
        print(response)
        pprint(response.json())
    
    def getUserInfo(self, username):
        response = requests.get(self.baseEndpoint + "users/" + username)
        pprint(response.json())
        return response.json()
        
    
    
