import unittest

from Profile import Profile
from user import UserLogin

from Recipe import Recipe

class ProfileTest(unittest.TestCase):
    def test(self):
        self.assertTrue(True)

    def test_getUserInfo(self):

        userInfoList = ["testName", "testSurame", "test@itu.edu.tr", "test123", "test14"]
        UserLogin.add_user(userInfoList[0], userInfoList[1], userInfoList[2], userInfoList[3],userInfoList[4])
        userInfo = Profile.get_userInfo("test123")

        self.assertEqual(userInfoList[0], userInfo[0][0])
        self.assertEqual(userInfoList[1], userInfo[0][1])
        self.assertEqual(userInfoList[2], userInfo[0][2])
        self.assertEqual(userInfoList[3], userInfo[0][5])

    



if __name__ == '__main__':
    unittest.main()
