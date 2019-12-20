from word import Word

class DataManager:
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
            return True
        except:
            return False

    def wordAdd(self, word):
        self.words.append(word)


    def readAllWords(self):
        tmp_wds = [
            ("word", "단어"),
            ("asd", "ㅁㄴㄹ"),
            ("qwer", "ㅂㅈㄷㄱ, ㅂㅈㄷㄱ"),
            ("zcxvzxcv",
             "ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ, ㅋㅌㅊㅍ"),
            ("rtyu", "ㄱ쇼ㅕ, ㄱ쇼ㅕ"),
            ("vbcbv", "ㅠㅊ풏ㅊ"),
            ("vbcbvyy", "ㅠㅊ풏ㅊㅊㅊ"),
            ("realword", "진짜 단어"),
            ("bback", "빡빡이아저씨"),
            ("aaaa", "아아아아"),
        ]

        for w in tmp_wds:
            self.words.append(Word(w[0], w[1], False))

        tmp_fwds = [
            ("focus", "집중하다"),
            ("wow", "놀라운"),
            ("amazing", "엄청난"),
            ("awesome", "개쩌는"),
            ("verylonglonglongandlongword", "매우 길고 길고 또 길고 그리고 긴 단어를 아주 길고 길게 적는중"),
        ]

        for w in tmp_fwds:
            ww = Word(w[0], w[1], True)
            self.words.append(ww)
            self.focusedWords.append(ww)

        print("Data Loaded")

    def saveAllWords(self):
        print("Data Saved")
