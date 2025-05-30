from scoring.scoreManager import ScoreManager, entry
from utils import User
from userBase import UserBase


def score_manager_init(ub):
    sc = ScoreManager(ub)
    return sc


def update_all_scores(sc):
    sc.updateAllScores()
    return 0


def right_grade(sc):
    for percent in sc.grade_percents:
        if sc.grade(percent + 0.01) is not sc.grade_percents[percent]:
            print("TEST FAILED at: ", percent)
            return -1
    print("TEST PASSED: right_grade")
    return 0


def add_new_user(sc):
    testUser = User(
        steamCode=76561198093909009,
        email="nickarmstrong888@gmail.com",
        discord="outvictus",
        nickname="Invictus",
    )
    # testUser = User(steamCode = "76561198082223836", nickname="Flamemaster") # Jacob
    sc.calculate_scores_for_user(testUser)
    print("score generated for user, ", testUser.lastScore)
    print("on Version: ", testUser.lastScoreVersion)
    return 0


# sometimes python pass by reference is stupid
def score_db_changes_on_calc(sc: ScoreManager, user: User):
    prev_score = entry(user.scores["achievement"], user.username)
    print("prev score: ", prev_score)
    print(sc.scores_db["achievement"])
    # assert prev_score in sc.scores_db["achievement"]
    sc.calculate_scores_for_user(user)
    new_score = user.scores["achievement"]
    print("new score: ", new_score)
    print(sc.scores_db["achievement"])
    # assert new_score in sc.scores_db["achievement"]
    # assert prev_score not in sc.scores_db["achievement"]
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


if __name__ == "__main__":
    ub = UserBase()
    testUser = ub.get_user_by_username("testUser10")
    sc = score_manager_init(ub)
    # add_new_user(sc)
    # right_grade(sc)
    # testRLScore()
    # testSteamScore()
    # testDotaScore()
    # testCSGOScore()
    # testTETRIOgetUserNameFromDiscord()
    # testCalculateTETRIOScore()
    # sc.user_base.print_all()
    # score_db_changes_on_calc(sc, testUser)
    fuckin_around_with_score_db(sc, testUser)
