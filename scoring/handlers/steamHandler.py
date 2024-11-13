import requests

from ..config import STEAM_KEY
from typing import List, Tuple
from ..calculators.dota import DotaScoreCalculator
from ..calculators.rocketLeague import rocketLeagueCalculator
from ..calculators.csgo import csgoCalculator
from ..calculators.steamAchievement import SteamAchievementScoreCalculator
from utils import init_calculator, Handler, ScoreCalculator

COMP_GAMES = {
    "570": DotaScoreCalculator,
    "252950": rocketLeagueCalculator,
    "730": csgoCalculator,
}


class SteamHandler(Handler):
    def __init__(self):
        self.KEY = STEAM_KEY
        self.compGames = {}
        # iterate through each of the necessary calculators and init one
        self.achievementCalc = SteamAchievementScoreCalculator()
        for appID in COMP_GAMES.keys():
            self.compGames[appID] = init_calculator(calculator=COMP_GAMES[appID])

    def get_scores(self, user) -> List[Tuple[str, float]]:
        scores = []
        userLibrary = self.get_user_library(user.accounts["steam"])
        achievementScore = self.achievementCalc.calculate_score(user, userLibrary)
        scores.append(("achievement", achievementScore))
        print("Steam achievement score: ", achievementScore)
        # Skipping comp games for now, will be added back later
        # for appID in userLibrary:
        #     if appID in self.compGames.keys():
        #         calc = self.compGames[appID]
        #         score = calc.calculate_score(user)
        #         scores.append((calc.name, score))
        #         print(calc.name, ": ", score)
        return scores

    # fetches the users library of games from the steam api
    def get_user_library(self, steamID) -> List[str]:
        response = requests.get(
            " http://api.steampowered.com/IPlayerService/GetOwnedGames/v001?key="
            + self.KEY
            + "&steamid="
            + str(steamID)
            + "&include_played_free_games"
        )
        if response.status_code == 403:
            print(
                "your account is private or has some privacy settings on, \
                      please fix and try again"
            )
            quit()
        if response.status_code == 400:
            print("non-valid steam code submitted")
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
