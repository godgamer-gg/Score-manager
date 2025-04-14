import requests
from utils import User, ScoreCalculator
import os


#  not implemented yet
class csgoCalculator(ScoreCalculator):

    name = "CSGO"
    TRN_KEY = os.getenv("TRN_KEY")

    def get_CSGO_score(self, steamID) -> int:
        print("getting CSGO score")
        response = requests.get(
            " https://public-api.tracker.gg/v2/csgo/standard/profile//v2/csgo/standard/profile/steam/"
            + steamID,
            headers={"TRN-Api-Key": TRN_KEY},
        )
        print(response)
        print(response.json())
        # self.pprint(response.json())
