import requests

from ScoreManager import ScoreCalculator
from utils import User
from config import TRN_KEY

#  not implemented yet
class csgoCalculator(ScoreCalculator):
    def getCSGOScore(self, steamID) -> int:
        print("getting CSGO score")
        response = requests.get(" https://public-api.tracker.gg/v2/csgo/standard/profile//v2/csgo/standard/profile/steam/" + steamID,
                                headers={"TRN-Api-Key":TRN_KEY})
        print(response)
        print(response.json())
        # self.pprint(response.json())