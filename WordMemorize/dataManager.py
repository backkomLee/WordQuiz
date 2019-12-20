import pickle
from word import Word
import time

class DataManager(object):
    def __init__(self):
        self.words = []
        self.focusedWords = []

        self.readAllWords()

    def getWords(self):
        return self.words

    def getFocusedWords(self):
        return self.focusedWords

    def wordDelete(self, word):
        try:
            self.words.remove(word)
            if word.getIsFocusing():
                self.focusedWords.remove(word)
            self.saveAllWords()
            return True
        except:
            return False

    def wordAdd(self, word):
        self.words.append(word)
        self.saveAllWords()

    def readAllWords(self):
        with open('words.txt', 'rb') as w:
            wds = pickle.load(w)
            for wd in wds:
                s = Word(wd[0], wd[1], (wd[2], self))
                self.words.append(s)


        print("Data Loaded")


    def saveAllWords(self):
        save = []
        for w in self.words:
            en, ko = w.getStrings()
            foc = w.getIsFocusing()
            save.append((en, ko, foc))

        with open('words.txt', 'wb') as w:
            pickle.dump(save, w)
        print("Data Saved")


    def readAllSettings(self):
        with open('settings.txt', 'rb') as w:
            sts = pickle.load(w)

        topic = sts[0]

        intervalStart = sts[1][0]
        intervalEnd = sts[1][1]

        print("Setting Loaded")
        return topic, intervalStart, intervalEnd


    def saveAllSettings(self, topic, interval):
        sts = []
        sts.append(topic)
        sts.append(interval)
        sts.append([(0, 0), (0, 0)])

        with open('settings.txt', 'wb') as w:
            pickle.dump(sts, w)
        print("Setting Saved")


if __name__ == '__main__':
    dm = DataManager()
    print(dm.readAllSettings())
    print(dm.words)
    time.sleep(0.5)
    dm.saveAllWords()
