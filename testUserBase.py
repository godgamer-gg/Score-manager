from manager import UserBase
from utils import User


def addAndGetUser():
    username = "testUser"
    password = "testUser"
    newUser = User(username, password)
    userID = newUser.userID
    userBase = UserBase()
    userBase.add_user(newUser)
    ret = userBase.get_user(userID)
    if ret.userID != userID:
        print("Wrong User ID")
        return -1
    
    if ret.username != username:
        print("Wrong username")
        return -1

    if ret.password != password:
        print("Wrong password")
        return -1
    
    print("Test PASSED")
    return 0






if __name__ == '__main__':
    # run test you want run
    addAndGetUser()