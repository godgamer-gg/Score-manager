import requests

from utils import User, ScoreCalculator

class rocketLeagueCalculator(ScoreCalculator):

    name = "RocketLeague"

    # Not properly implemented yet
    def getRLScore(self, steamID) -> int:
        print('getting rocket league competitive score')
        print("can't access it yet")
        return 0
        response = requests.get("https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/" + steamID)
        print(response)
        response = requests.get("https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/76561198093909009&key=" + self.KEY)
        print(response)
        pprint(response.json())
        # self.pprint(response.json())