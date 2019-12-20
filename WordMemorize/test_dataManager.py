import unittest
from dataManager import DataManager
from word import Word


def isListSame(lst1, lst2):
    if len(lst1) != len(lst2):
        return False

    for i in range(len(lst1)):
        if lst1[i] != lst2[i]:
            return False
    else:
        return True

def isListSameOfIsWordSame(lst1, lst2):
    if len(lst1) != len(lst2):
        return False

    for i in range(len(lst1)):
        if not isWordSame(lst1[i], lst2[i]):
            return False
    else:
        return True

def isWordSame(wd1, wd2):
    return wd1.en == wd2.en and wd1.ko == wd2.ko and wd1.isFocusing == wd2.isFocusing


class TestWord(unittest.TestCase):
    def setUp(self):
        self.d1 = DataManager()

        self.wd1 = Word('software', '소프트웨어', (True, self.d1))
        self.wd2 = Word('project', '프로젝트', (True, self.d1))

        self.d1.words = [self.wd1, self.wd2]

    def tearDown(self):
        pass

    def testWords(self):
        wd3 = Word('clear', '끝')
        self.d1.wordAdd(wd3)
        self.assertEqual(self.d1.getWords(), [self.wd1, self.wd2, wd3])

        wd4 = Word('bye', '안녕')
        self.d1.wordAdd(wd4)
        self.assertTrue(isListSame(self.d1.getWords(), [self.wd1, self.wd2, wd3, wd4]))
        self.d1.wordDelete(self.wd2)
        self.assertTrue(isListSame(self.d1.getWords(), [self.wd1, wd3, wd4]))
        self.d1.wordDelete(wd4)
        self.assertTrue(isListSame(self.d1.getWords(), [self.wd1, wd3]))
        self.assertTrue(isListSame(self.d1.getFocusedWords(), [self.wd1]))

        self.d1.saveAllWords()
        self.d1.readAllWords()
        self.assertTrue(isListSameOfIsWordSame(self.d1.getWords(), [self.wd1, wd3]))
        self.assertTrue(isListSameOfIsWordSame(self.d1.getFocusedWords(), [self.wd1]))


if __name__ == '__main__':
   unittest.main()