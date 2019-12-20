class Word(object):
    def __init__(self, en, ko, foc):
        self.en = en
        self.ko = ko
        self.isFocusing = foc

    def getStrings(self):
        return self.en, self.ko

    def getIsFocusing(self):
        return self.isFocusing

    def setIsFocusing(self, foc, dataManager):
        self.isFocusing = foc
        dataManager.saveAllWords()

    # def __str__(self):
    #     return "\'" + self.en + " : " + self.ko + "\'"

