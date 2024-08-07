from calculators.steamAchievement import SteamAchievementScoreCalculator
from calculators.webGameCalculators import TETRIOCalculator
from scoring.ScoreManager import ScoreManager
from ..utils import User

def scoreManagerInit():
    sc = ScoreManager()
    return sc

def runUpdateAllScores(sc):
    sc.updateAllScores()
    return 0

def addNewUser(sc):
    testUser = User(steamCode=76561198093909009, email="nickarmstrong888@gmail.com", discord="outvictus", nickname="Invictus")
    # testUser = User(steamCode = "76561198082223836", nickname="Flamemaster") # Jacob
    sc.calculateScoresForUser(testUser)
    print("score generated for user, ", testUser.lastScore)
    print ("on Version: ", testUser.lastScoreVersion)
    return 0

# def testSteamScore():
#     sif = steamInfoFetcher()
#     # sif.calculateTotalScore("") # Name
#     # sif.calculateTotalScore("76561198093909009") # Me
#     # sif.calculateTotalScore("76561198118212860") # Alex
#     # sif.calculateTotalScore("76561198082223836") # Jacob
#     # sif.calculateTotalScore("76561198036298829") # George
#     # sif.calculateTotalScore("76561198999006815") # Anna
#     # sif.calculateTotalScore("76561198047686785") # Ziggy
#     # sif.calculateTotalScore("76561198018040884") # Ray
#     # sif.calculateTotalScore("76561198139518527") # Kevin
#     # sif.calculateTotalScore("76561198000265730") # Taylor
#     # sif.calculateTotalScore("76561197978063214") # Kyle
#     # sif.calculateTotalScore("76561198066947995") # Dreamboiz

# def testDotaScore():
#      sif = steamInfoFetcher()
#     #  sif.getDOTAScore("76561197978063214") # Kyle
#     #  sif.getDOTAScore("76561198066947995") # Dreamboiz
#      sif.getDOTAScore("76561198082223836") # Jacob

# def testRLScore():
#     sif = steamInfoFetcher()
#     sif.getRLScore("76561198093909009") # Me

# def testCSGOScore():
#     sif = steamInfoFetcher()
#     sif.getCSGOScore("76561198093909009") # Me

def testTETRIOgetUserNameFromDiscord():
    tetr = TETRIOCalculator()
    username = tetr.getUserNameFromDiscord("flamemaster73")
    print(username)

def testCalculateTETRIOScore():
    tetr = TETRIOCalculator()
    score = tetr.calculateScore("Invictus")
    print(score)


def testRiotScore():
    print("TODO")

if __name__ == '__main__':
    sc = scoreManagerInit()
    addNewUser(sc)
    # testRLScore()
    # testSteamScore()
    # testDotaScore()
    # testCSGOScore()
    # testTETRIOgetUserNameFromDiscord()
    # testCalculateTETRIOScore()