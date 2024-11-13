import jsonpickle
import string
import random
from manager import UserBase
from utils import User
from pprint import pprint


def add_and_get_user():
    username = "testUser"
    password = "testUser"
    user = User(username, password)
    userID = user.userID
    user_base = UserBase()
    user_base.add_user(user)
    ret = user_base.get_user(userID)
    if ret.userID != userID:
        print("Wrong User ID")
        return -1

    if ret.username != username:
        print("Wrong username")
        return -1

    if ret.password != password:
        print("Wrong password")
        return -1

    user_base.delete_user(userID)
    print("Test PASSED: add_and_get_user")
    return 0


# adds a user and doesn't delete for when this is helpful
def add_a_user():
    username = "".join(random.choices(string.ascii_letters, k=7))
    password = "".join(random.choices(string.ascii_letters, k=7))
    user = User(username, password)
    user.accounts["steam"] = 12345678
    user.accounts["discord"] = "mrUser"
    user_base = UserBase()
    user_base.add_user(user)
    return 0


def store_load_user():
    #  create user
    username = "testUser"
    password = "testUser"
    user = User(username, password)
    user.accounts["steam"] = 12345678
    user.accounts["discord"] = "test"
    UID = user.userID

    #  add and store user
    user_base_a = UserBase()
    user_base_a.add_user(user)
    user_base_a.store_all()

    #  create a new UserBase, which should load the newly created user
    user_base_b = UserBase()
    ret_user = user_base_b.get_user(UID)
    print(ret_user.accounts)
    if ret_user.accounts != user.accounts:
        print("Accounts not the same")
        return -1

    user_base_a.delete_user(UID)
    print(ret_user.accounts)
    print(user.accounts)

    print("TEST PASSED: store_load_user")
    return 0


def set_load_score():
    username = "".join(random.choices(string.ascii_letters, k=7))
    password = "".join(random.choices(string.ascii_letters, k=7))
    test_user = User(username, password)
    UID = test_user.userID
    scores = {"steam": 100, "riot": 100}
    test_user.scores = scores
    test_user.last_score_version = "test_version"
    user_base = UserBase()
    user_base.add_user(test_user)
    user_base.load_users()
    ret_user = user_base.get_user(UID)
    if ret_user.scores != test_user.scores:
        pprint("ret user scores: ", ret_user.scores)
        pprint("test user scores: ", test_user.scores)
        return -1
    if ret_user.last_score_version is not test_user.last_score_version:
        print("ret user", ret_user.last_score_version)
        print("test user", test_user.last_score_version)
        return -1
    user_base.delete_user(UID)
    print("TEST PASSED: set_load_score")
    return 0


def test_encoding():
    username = "testUser"
    password = "testUser"
    user = User(username, password)
    user.accounts["steam"] = 12345678
    user.accounts["discord"] = "test"
    UID = user.userID
    # settings to make sure jsonpickle will properly function
    jsonpickle.set_encoder_options("json", sort_keys=True)
    jsonpickle.register(User)
    # Force jsonpickle to fully encode custom objects and dictionaries
    jsonpickle.set_encoder_options("json", unpicklable=True)

    json_str = jsonpickle.encode(user)
    print("updating user: ", user.username)
    print(json_str)
    ret_user = jsonpickle.decode(json_str)
    print(ret_user.accounts)
    return 0


def print_all():
    user_base = UserBase()
    user_base.print_all()
    return 0


def clean():
    user_base = UserBase()
    user_base.clean()
    return 0


if __name__ == "__main__":
    # run test you want run
    # store_load_user()
    # add_and_get_user()
    # test_encoding()
    # add_a_user()
    # set_load_score()
    # clean()
    print_all()
