import requests

class riotScoreCalculator:

    def __init__():
        # needs to be regenerated daily
        self.KEY = "RGAPI-2ddd1d01-c759-409f-a336-db0a0f3044cd"

    def calculateRawScore():
        # for rank data use league-v4 to get the neccsarry ids that you need you'll 
        # have to get the players puuid using account-v1 (puuid is what you need for 
        # match-v5) and the summonerid that you need for leaguev4 you can get using 
        # summoner-v4 by supplying it with the puuid you got from account-v1
