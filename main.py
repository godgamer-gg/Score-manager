from steamScoreCalculators import steamAchievementScoreCalculator

CALCULATORS = [
    steamAchievementScoreCalculator,
]

# Use this as a base class for any new calculator
class ScoreCalculator():
    
    def calculateScore():
        pass

# TODO: literally everything - I'll get back to this one later
class profileHandler():

    def __init__(self):
        self.profiles = dict()

    def createProfile(self, username, info):
        self.profiles[username] = info
    
    def getProfile(self, username): # -> dict[str, str]: this makes pylance angry, not sure why
        return self.profiles[username]


def main():
    pH = profileHandler()



if __name__ == '__main__':
    main()