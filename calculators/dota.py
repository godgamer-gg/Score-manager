import requests
from utils import COMP_MAX_SCORE, User, ScoreCalculator

DOTA_COMP_GROWTH_EXP = 1.41 # exponent for increase in ranks
DOTA_CHAR_GROWTH_Factor = 5 # exponent for increase in character value
DOTA_CHAR_GROWTH_SCALE = 100
DOTA_SPLIT = .7 # 70% of the score is rank, 30% is from individual character scores

class DotaScoreCalculator(ScoreCalculator):

    name = "DOTA"

    # gets the player's current rank in DOTA
    def calculateScore(self, user: User) -> int:
        steamID = user.accounts["steam"]
        print("getting Dota Competitive Score")
        # This is the same as the users friend code, basically outdated steamIDs
        dotaID = int(steamID) - 76561197960265728
        response = requests.get("https://api.opendota.com/api/players/" + str(dotaID))
        rank_tier = response.json()['rank_tier']

        rank_score = (2**(rank_tier / 10)) * (COMP_MAX_SCORE/(80**DOTA_COMP_GROWTH_EXP)) * DOTA_SPLIT

        # I don't have a sample on this so I have no idea how to scale it properly
        rank_score += response.json()['rank_tier'] * 1000

        # individual characters score
        # This will need a complete refactor but is honestly fine for now
        response = requests.get("https://api.opendota.com/api/players/" + str(dotaID) + "/rankings")
        char_score = 0
        for hero in response.json():
            prc = hero['percent_rank']
            if prc > .6:
                score = (((prc - .6) * 100) * DOTA_CHAR_GROWTH_Factor)
            else:
                score = 0
            char_score += score
            # raw_score += (10000 / val**GROWTH_EXP) + BONUS_PTS
        max_char_score = COMP_MAX_SCORE * (1 - DOTA_SPLIT)
        if char_score > max_char_score: char_score = max_char_score
        total_score = rank_score + char_score
        print("DOTA scores: ", rank_score, ", ", char_score, ", ", total_score)
        return total_score