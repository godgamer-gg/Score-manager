# Gets achievements for each user and the game they have played

# philosophy - we can't compare games so each game must have a max score possible
# E.g the best player of game A should be treated as the best player of game B
# nuance in a player's rank is built up through their scores across games
# Flaw: the cap/growth has to be very high such that being mediocre in a bunch of games
# isn't enough to equal being the best of one game

import requests
from utils import pprint, User, ACHIEV_MAX_SCORE
from config import STEAM_KEY
from ScoreManager import ScoreCalculator

COMPLETION_BONUS = 1.3
GROWTH_EXP = 1.41
BONUS_PTS = 2

class SteamAchievementScoreCalculator(ScoreCalculator):
    def __init__(self):
        pass

    # points = Sum((100^ / (rarity %)^(growth rate)) + (bonus)
    # fully completing a game results in an additional bonus score, likely a 20% increase to points across the board
    def calculateScore(self, user: User) -> float:
        steamID = user.accounts["steam"]
        gameIDs = self.getUserLibrary(steamID)
        total_score = 0
        achiev_total_score = 0
        comp_total_score = 0
        gameIDs = ["570"]
        for appID in gameIDs:
            # Achievement Score
            percents, completed = self.getAchievementsForGame(appID, steamID)
            if len(percents) > 0:
                achiev_score = self.calculateScoreForGame(percents)
                if completed:
                    achiev_score = achiev_score * COMPLETION_BONUS
                achiev_score = ACHIEV_MAX_SCORE if achiev_score > ACHIEV_MAX_SCORE else achiev_score
                achiev_total_score += achiev_score
                total_score += achiev_score
                print(appID, " achievement score: ", achiev_score)
            
            # Competitive Score
            if appID in self.comp_Games.keys():
                comp_score = self.comp_Games[appID](steamID)
                comp_total_score += comp_score
                total_score += comp_score
                print(appID, " competitive score: ", comp_score)

        total_score = round(total_score, 3)
        print("achievement total score: ", round(achiev_total_score, 3))
        print("Competitive total score: ", round(comp_total_score, 3))
        print("Total Score: ", total_score)
        return total_score
    
    def getUserLibrary(self, steamID) -> list[str]:
        response = requests.get(" http://api.steampowered.com/IPlayerService/GetOwnedGames/v001?key=" 
                                + STEAM_KEY + "&steamid=" + steamID + "&include_played_free_games")
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

    def getAchievementsForGame(self, appID, steamID) -> (list[float], bool):
        # get the achievements the player has for the game
        response = requests.get("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid="
                                + appID + "&key=" + STEAM_KEY + "&steamid=" + steamID)
        if response.status_code == 403:
            print("your account is private or has some privacy settings on, \
                      please fix and try again")
            quit()
        achievements = list()
        try:
            data = response.json()['playerstats']['achievements']
        except KeyError:
            return [], 0 # game has no achievements

        for entry in data:
            if entry['achieved']:
                achievements.append(entry['name'])

        # get the global completion percentages for each achievement for a game
        response = requests.get("http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=" + appID)
    
        if response.status_code == 403:
            print("your account is private or has some privacy settings on, \
                      please fix and try again")
            quit()

        # check if the player has completed every possible achievement
        all_achieve_and_percents = response.json()['achievementpercentages']['achievements']
        
        # turning the list of (name, percent) into a dictionary to make things easier and faster
        d = dict()
        for entry in all_achieve_and_percents:
            d[entry['name']] = entry['percent']
        
        percents = list()
        if set(achievements) == d.keys():
            # if they are equal we can just go ahead and put all of the percents and finish
            for entry in all_achieve_and_percents:
                percents.append(entry['percent'])
            return percents, True
        else:
            for ach in achievements:
                if ach in d.keys():
                    percents.append(d[ach])
            return percents, False
    
    def calculateScoreForGame(self, percents):

        # sum up the value for each achievement
        raw_score = 0
        for val in percents:
            raw_score += (10000 / val**GROWTH_EXP) + BONUS_PTS
        return raw_score
    