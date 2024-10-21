import requests
from utils import pprint, ScoreCalculator


class TETRIOCalculator(ScoreCalculator):

    name = "TETRIO"

    def __init__(self):
        self.baseEndpoint = "https://ch.tetri.io/api/"

    def calculate_score(self, username):
        self.getUserInfo(username)

    def get_user_name_from_discord(self, discord) -> str:
        response = requests.get(self.baseEndpoint + "users/search/discord" + discord)
        print(response)
        pprint(response.json())

    def get_user_info(self, username):
        response = requests.get(self.baseEndpoint + "users/" + username)
        pprint(response.json())
        return response.json()
