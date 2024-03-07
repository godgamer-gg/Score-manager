from steamInfo import steamInfoFetcher

class ScoreCalculator():

    def calculateScore():
        steam = steamInfoFetcher
        steam.testSteamScore()

class profileHandler():

    def __init__(self):
        self.profiles = dict()

    def createProfile(self, username, info):
        print("creating profile for: ", username)
        self.profiles[username] = info
    
    def getProfile(self, username) -> dict[str: str]:
        return self.profiles[username]


def main():
    pH = profileHandler()



if __name__ == '__main__':
    main()