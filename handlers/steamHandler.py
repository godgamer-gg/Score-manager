import requests

from config import STEAM_KEY
from ScoreManager import Handler, ScoreCalculator
from calculators.dota import DotaScoreCalculator
from calculators.rocketLeague import rocketLeagueCalculator
from calculators.csgo import csgoCalculator

COMP_GAMES = {
    "570" : DotaScoreCalculator,
    "252950": rocketLeagueCalculator,
    "730": csgoCalculator
}

class SteamHandler(Handler):
    def __init__(self):
        self.KEY = STEAM_KEY
        self.comp_Games = {
            "570" : self.getDOTAScore,
            "252950": self.getRLScore,
            "730": self.invalid_Comp_Func
        }
    
    def initCalculator(self, calculator: type[ScoreCalculator]) -> ScoreCalculator:
        
    
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