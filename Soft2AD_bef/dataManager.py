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
                s = Word(wd[0], wd[1], wd[2])
                self.words.append(s)
                if wd[2]:
                    self.focusedWords.append(s)

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


    def realAllSettings(self):
        with open('settings.txt', 'rb') as w:
            sts = pickle.load(w)

        print("Setting Loaded")
        return sts


    def saveAllSettings(self, sts):
        with open('settings.txt', 'wb') as w:
            pickle.dump(sts, w)
        print("Setting Saved")



if __name__ == '__main__':
    dm = DataManager()
    print(dm.realAllSettings())
    print(dm.words)
    time.sleep(0.5)
    dm.saveAllWords()

    '''
            tmp_wds = [
                ('frozen', '겨울왕국', True),
                ('unknown', '알려지지 않은', True),
                ('software', '소프트웨어', False),
                ('calculate', '계산하다', False),
                ('Pneumonoultramicroscopicsilicovolcanoconiosis', '주로 화산에서 발견되는 아주 미세한 규소 먼지를 흡입하여 허파에 쌓여 생기는 만성 폐질환', False)
            ]

            for w in tmp_wds:
                self.words.append(Word(w[0], w[1], w[2]))
                if w[2]:
                    self.focusedWords.append(w)
            '''

    '''
    
        sts = [
            "damin1009",
            (1, 1),
            [(0, 0), (0, 0)]
        ]

        return sts
    
    '''