from steamInfo import steamInfoFetcher
from webGameCalculators import TETRIOCalculator

def testSteamScore():
    sif = steamInfoFetcher()
    # sif.calculateTotalScore("") # Name
    # sif.calculateTotalScore("76561198093909009") # Me
    # sif.calculateTotalScore("76561198118212860") # Alex
    # sif.calculateTotalScore("76561198082223836") # Jacob
    # sif.calculateTotalScore("76561198036298829") # George
    # sif.calculateTotalScore("76561198999006815") # Anna
    # sif.calculateTotalScore("76561198047686785") # Ziggy
    # sif.calculateTotalScore("76561198018040884") # Ray
    # sif.calculateTotalScore("76561198139518527") # Kevin
    # sif.calculateTotalScore("76561198000265730") # Taylor
    # sif.calculateTotalScore("76561197978063214") # Kyle
    # sif.calculateTotalScore("76561198066947995") # Dreamboiz

def testDotaScore():
     sif = steamInfoFetcher()
    #  sif.getDOTAScore("76561197978063214") # Kyle
    #  sif.getDOTAScore("76561198066947995") # Dreamboiz
     sif.getDOTAScore("76561198082223836") # Jacob

def testRLScore():
    sif = steamInfoFetcher()
    sif.getRLScore("76561198093909009") # Me

def testCSGOScore():
    sif = steamInfoFetcher()
    sif.getCSGOScore("76561198093909009") # Me

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
    # testRLScore()
    # testSteamScore()
    # testDotaScore()
    # testCSGOScore()
    # testTETRIOgetUserNameFromDiscord()
    testCalculateTETRIOScore()