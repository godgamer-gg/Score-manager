# High level system tests
from manager import Manager, UserBase
from utils import User


# just creates the manager but also acts as a test
def init_manager():
    try:
        manager = Manager()
    except Exception as e:
        print("TEST FAILED: init_manager: ", e)
        return -1
    print("TEST PASSED: init_manager")
    return manager


# coming back to this one
def calc_score_sets_scores():
    manager = Manager()
    return 0


def calc_user_scores(m: Manager):
    # grab a test user
    # calc scores for that user
    # make scores are as expected
    username = "testUser10"
    scores = m.calculate_user_scores(username)
    print(scores)


def get_user_score_breakdown(m: Manager):
    username = "Alex"
    scores = m.get_user_score_breakdown(username)
    print(scores)


if __name__ == "__main__":
    # run tests
    manager = init_manager()
    # calc_score_sets_scores()
    # calc_user_scores(manager)
    get_user_score_breakdown(manager)
