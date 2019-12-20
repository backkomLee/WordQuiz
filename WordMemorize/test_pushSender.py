import unittest
import time

from pushSender import PushSender
from test_dataManager import DataManager
from word import Word

class TestSearchEnglish(unittest.TestCase):
    def setUp(self):
        dataM = DataManager()

        self.sender = PushSender(dataM, "damin1009")
        self.sender.pushSend(Word("Hello", "안녕?", (True, dataM)))
        self.sender.pushSendingThreadStart()

    def tearDown(self):
        pass

    def testSearchEnglish(self):
        self.sender.setWaitTime(1, 2)
        self.assertEqual(self.sender.waitTimeMin, 60)
        self.assertEqual(self.sender.waitTimeMax, 120)
        self.sender.setWaitTime(1, 1)
        self.assertEqual(self.sender.waitTimeMin, 60)
        self.assertEqual(self.sender.waitTimeMax, 61)
        self.sender.setWaitTime(1, 0)
        self.assertEqual(self.sender.waitTimeMin, 60)
        self.assertEqual(self.sender.waitTimeMax, 61)

if __name__ == '__main__':
    unittest.main()