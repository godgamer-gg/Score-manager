import requests

from config import STEAM_KEY
from ScoreManager import Handler, ScoreCalculator
from calculators.dota import DotaScoreCalculator
from calculators.rocketLeague import rocketLeagueCalculator
from calculators.csgo import csgoCalculator
from utils import initCalculator

COMP_GAMES = {
    "570" : DotaScoreCalculator,
    "252950": rocketLeagueCalculator,
    "730": csgoCalculator
}

class SteamHandler(Handler):
    def __init__(self):
        self.KEY = STEAM_KEY
        self.compGames = {}
        # iterate through each of the necessary calculators and init one
        for appID in COMP_GAMES.keys():
            self.compGames[appID] = initCalculator(COMP_GAMES[appID])

    
    def getUserLibrary(self, steamID) -> list[str]:
        response = requests.get(" http://api.steampowered.com/IPlayerService/GetOwnedGames/v001?key=" 
                                + self.KEY + "&steamid=" + steamID + "&include_played_free_games")
        if response.status_code == 403:
            print("your account is private or has some privacy settings on, \
                      please fix and try again")
            quit()
        json = response.json()
        gameIDs = list()
        try: 
            for game in json["response"]["games"]:
                gameIDs.append(str(game["appid"]))
        except KeyError:
            print("Your library is not set to public, please fix and try again")
            quit()
            
        return gameIDs