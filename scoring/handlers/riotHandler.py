import requests
from ..config import RIOT_KEY
from ..utils import Handler

class RiotHandler(Handler):

    def __init__(self):
        # needs to be regenerated daily
        self.KEY = RIOT_KEY

    def calculateRawScore():
        # for rank data use league-v4 to get the neccsarry ids that you need you'll 
        # have to get the players puuid using account-v1 (puuid is what you need for 
        # match-v5) and the summonerid that you need for leaguev4 you can get using 
        # summoner-v4 by supplying it with the puuid you got from account-v1
        print("TODO")
