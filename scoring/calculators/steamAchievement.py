# Gets achievements for each user and the game they have played

# philosophy - we can't compare games so each game must have a max score possible
# E.g the best player of game A should be treated as the best player of game B
# nuance in a player's rank is built up through their scores across games
# Flaw: the cap/growth has to be very high such that being mediocre in a bunch of games
# isn't enough to equal being the best of one game

import requests
import os
from typing import List, Tuple
from utils import pprint, User, ACHIEV_MAX_SCORE, ScoreCalculator

COMPLETION_BONUS = 1.3
GROWTH_EXP = 1.41
BONUS_PTS = 2

STEAM_KEY = os.getenv("STEAM_KEY")


class SteamAchievementScoreCalculator(ScoreCalculator):
    def __init__(self):
        pass

    # points = Sum((100^ / (rarity %)^(growth rate)) + (bonus)
    # fully completing a game results in an additional bonus score, likely a 20% increase to points across the board
    def calculate_score(self, user: User, gameIDs) -> float:
        print("calculating achievement score")
        steamID = user.accounts["steam"]
        total_score = 0
        achiev_total_score = 0
        for appID in gameIDs:
            # Achievement Score
            percents, completed = self.get_achievements_for_game(appID, steamID)
            if len(percents) > 0:
                achiev_score = self.calculate_score_for_game(percents)
                if completed:
                    achiev_score = achiev_score * COMPLETION_BONUS
                achiev_score = (
                    ACHIEV_MAX_SCORE
                    if achiev_score > ACHIEV_MAX_SCORE
                    else achiev_score
                )
                achiev_total_score += achiev_score
                total_score += achiev_score
                # print(appID, " achievement score: ", achiev_score)

        total_score = round(total_score, 3)
        return total_score

    # returns a list of achievements completion percentages for each achievement the player has acquired,
    # along with true if the player has every achievement for the game
    def get_achievements_for_game(self, appID, steamID) -> Tuple[List[float], bool]:
        # get the achievements the player has for the game
        response = requests.get(
            "http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid="
            + appID
            + "&key="
            + STEAM_KEY
            + "&steamid="
            + str(steamID)
        )
        if response.status_code == 403:
            print(
                "your account is private or has some privacy settings on, \
                      please fix and try again"
            )
            quit()
        achievements = list()
        try:
            data = response.json()["playerstats"]["achievements"]
        except KeyError:
            return [], 0  # game has no achievements

        for entry in data:
            if entry["achieved"]:
                achievements.append(entry["name"])

        # get the global completion percentages for each achievement for a game
        response = requests.get(
            "http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid="
            + appID
        )

        if response.status_code == 403:
            print(
                "your account is private or has some privacy settings on, \
                      please fix and try again"
            )
            quit()

        # check if the player has completed every possible achievement
        all_achieve_and_percents = response.json()["achievementpercentages"][
            "achievements"
        ]

        # turning the list of (name, percent) into a dictionary to make things easier and faster
        d = dict()
        for entry in all_achieve_and_percents:
            d[entry["name"]] = entry["percent"]

        percents = list()
        if set(achievements) == d.keys():
            # if they are equal we can just go ahead and put all of the percents and finish
            for entry in all_achieve_and_percents:
                percents.append(entry["percent"])
            return percents, True
        else:
            for ach in achievements:
                if ach in d.keys():
                    percents.append(d[ach])
            return percents, False

    def calculate_score_for_game(self, percents):

        # sum up the value for each achievement
        raw_score = 0
        for val in percents:
            raw_score += (10000 / float(val) ** GROWTH_EXP) + BONUS_PTS
        return raw_score
