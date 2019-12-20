class Word(object):
    def __init__(self, en, ko, foc=None):
        self.en = en
        self.ko = ko
        self.isFocusing = False

        if foc is not None:
            if foc[0]:  # focusing 단어라면
                self.setIsFocusing(foc[0], foc[1])


    def getStrings(self):
        return self.en, self.ko

    def getIsFocusing(self):
        return self.isFocusing

    def setIsFocusing(self, foc, dataManager):
        if foc == self.isFocusing:
            return

        self.isFocusing = foc
        try:
            if self.isFocusing:
                dataManager.getFocusedWords().append(self)
            else:
                dataManager.getFocusedWords().remove(self)
        except:
            pass

        dataManager.saveAllWords()


