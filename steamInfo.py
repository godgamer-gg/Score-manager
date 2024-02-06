# Gets achievements for each user and the game they have played

import requests

COMPLETION_BONUS = 1.2
GROWTH_RATE = 1.5
BONUS_PTS = 3

class steamInfoFetcher():
    def __init__(self):
        self.KEY = "DDBDBC9CE41A708C9B190F7DE5F0EE97"

    # First find the players account

    # Next find the list of games the player has

    # Get the achievements the player has obtained

    # Output a score based on achievement percentages and number of total players of 
    # the game
    # The more players that play a game and the less that obtain a certain achievement 
    # the more it is worth
    # points = Sum((100^ / (rarity %)^(growth rate)) + (bonus)
    # fully completing a game results in an additional bonus score, likely a 20% increase to points across the board

# http://api.steampowered.com/<interface name>/<method name>/v<version>/?key=<api key>&format=<format>

    def calculateTotalScore(self, steamID) -> float:
        gameIDs = self.getUserLibrary(steamID)
        score = 0
        for appID in gameIDs:
            percents, completed = self.getAchievementsForGame(appID, steamID)
            if len(percents) > 0:
                score += self.calculateScoreForGame(percents, completed, appID)
        score = round(score, 3)
        print("total score: " + str(score))
        return score
    
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
    
    def calculateScoreForGame(self, percents, appID, completed):

        # sum up the value for each achievement
        raw_score = 0
        for val in percents:
            raw_score += (10000 / val**GROWTH_RATE) + BONUS_PTS

        # 20% increase for full completion
        if completed:
            raw_score = raw_score * COMPLETION_BONUS
        #appId isn't used now because I don't have a way of getting popularity of a game 
        print(raw_score)
        return raw_score
        
        