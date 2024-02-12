# Gets achievements for each user and the game they have played

# philosophy - we can't compare games so each game must have a max score possible
# E.g the best player of game A should be treated as the best player of game B
# nuance in a player's rank is built up through their scores across games
# Flaw: the cap/growth has to be very high such that being mediocre in a bunch of games
# isn't enough to equal being the best of one game

import requests
import json

COMPLETION_BONUS = 1.3
GROWTH_EXP = 1.41
BONUS_PTS = 2

DOTA_COMP_GROWTH_EXP = 1.41 # exponent for increase in ranks
DOTA_CHAR_GROWTH_Factor = 5 # exponent for increase in character value
DOTA_CHAR_GROWTH_SCALE = 100
DOTA_SPLIT = .7 # 70% of the score is rank, 30% is from individual character scores

COMP_MAX_SCORE = 300000 # Maximum value each comp game can produce for getting to the max rank

ACHIEV_MAX_SCORE = 100000

class steamInfoFetcher():
    def __init__(self):
        self.KEY = "DDBDBC9CE41A708C9B190F7DE5F0EE97"
        self.comp_Games = {
            "570" : self.getDOTAScore,
            "252950": self.getRLScore,
            "730": self.invalid_Comp_Func
        }

    # points = Sum((100^ / (rarity %)^(growth rate)) + (bonus)
    # fully completing a game results in an additional bonus score, likely a 20% increase to points across the board
    def calculateTotalScore(self, steamID) -> float:
        gameIDs = self.getUserLibrary(steamID)
        total_score = 0
        achiev_total_score = 0
        comp_total_score = 0
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

    def getAchievementsForGame(self, appID, steamID) -> (list[float], bool):
        # get the achievements the player has for the game
        response = requests.get("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid="
                                + appID + "&key=" + self.KEY + "&steamid=" + steamID)
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
    
    # gets the player's current rank in DOTA
    def getDOTAScore(self, steamID) -> int:
        print("getting Dota Competitive Score")
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

    def getRLScore(self, steamID) -> int:
        print('getting rocketleague competitive score')
        print("can't access it yet")
        return 0
        response = requests.get("https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/" + steamID)
        print(response)
        response = requests.get("https://api.tracker.gg/api/v2/rocket-league/standard/profile/steam/76561198093909009&key=" + self.KEY)
        print(response)
        self.pprint(response.json())
        # self.pprint(response.json())

    def pprint(self, data):
        json_str = json.dumps(data, indent=4)
        print(json_str)
        
        
    def invalid_Comp_Func(self, steamID):
        print("game does not have a competitive score implemented yet")
        return 0
    