import random
import pickle

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLayout, QGridLayout
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QToolButton, QComboBox, QLabel, QScrollArea, QGroupBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QMessageBox, QCheckBox, QTimeEdit

from word import Word
from dataManager import DataManager
from webCrawler import WebCrawler
from pushSender import PushSender

class WindowsManager:
    def __init__(self, pushsendingstart):
        self.dataManager = DataManager()
        sts = self.dataManager.realAllSettings()

        self.webCrawler = WebCrawler()
        self.pushSender = PushSender(self.dataManager, "wowawesome")

        if pushsendingstart:
            self.pushSender.pushSendingThreadStart()

        self.nowListedWords = self.getAllWords()

        self.mainWindow = MainWindow(self)
        self.memorizeWindow = MemorizeWindow(self)
        self.settingWindow = SettingWindow(self)
        self.settingWindow.settingLoad(sts)

        self.mainWindow.showWindow()
        self.memorizeWindow.hideWindow()
        self.settingWindow.hide()

    def getAllWords(self):
        return self.dataManager.getWords()

    def setNowListedWords(self, to_this):
        self.nowListedWords = to_this

    def getNowListedWords(self):
        return self.nowListedWords

    def memorizeModeStart(self):
        self.mainWindow.hideWindow()
        self.memorizeWindow.showWindow()

    def memorizeModeEnd(self):
        self.mainWindow.showWindow()
        self.memorizeWindow.hideWindow()
        # self.mainWindow.updateListedWords()

    def qButtonMaker(self, name, callback, fixedSize=None, sizePolicy=None):
        bt = QToolButton()
        bt.setText(name)
        bt.clicked.connect(callback)

        if fixedSize is not None:
            wid, hei = fixedSize
            if wid == -1:
                bt.setFixedHeight(hei)
            elif hei == -1:
                bt.setFixedWidth(wid)
            else:
                bt.setFixedSize(fixedSize[0], fixedSize[1])

        if sizePolicy is not None:
            bt.setSizePolicy(sizePolicy[0], sizePolicy[1])

        return bt

    def qTextWidgetSetter(self, widget, startText, isReadOnly, alignment=None, fixedSize=None, sizePolicy=None, fontSizeUp=0):
        widget.setText(startText)
        widget.setReadOnly(isReadOnly)

        if alignment is not None:
            widget.setAlignment(alignment)

        if fixedSize is not None:
            wid, hei = fixedSize
            if wid == -1:
                widget.setFixedHeight(hei)
            elif hei == -1:
                widget.setFixedWidth(wid)
            else:
                widget.setFixedSize(fixedSize[0], fixedSize[1])

        if sizePolicy is not None:
            widget.setSizePolicy(sizePolicy[0], sizePolicy[1])

        if fontSizeUp != 0:
            font = widget.font()
            font.setPointSize(font.pointSize() + fontSizeUp)
            widget.setFont(font)

        return widget

    #def __del__(self):
    #    self.dataManager.saveAllWords()


class MainWindow(QWidget):
    def __init__(self, windowsManager, parent=None):
        super().__init__(parent)
        self.windowsManager = windowsManager

        # 툴바 레이아웃. 상단에 단어 정렬, 설정, 외우기모드 시작 버튼 등
        # 조작할 수 있는 것들을 모아둠.
        toolbarLayout = QGridLayout()

        memorizeStartBt = self.windowsManager.qButtonMaker(
            "Memorize Start", self.buttonClicked, None, (QSizePolicy.Expanding, QSizePolicy.Expanding))
        toolbarLayout.addWidget(memorizeStartBt, 0, 0, 3, 1)

        self.wordStandardCB = QComboBox()
        self.wordStandardCBStarted = False
        self.wordStandardCB.currentIndexChanged.connect(self.wordStandardCBChanged)
        self.wordStandardCB.addItems(["모두", "집중 단어만", "집중 단어 아닌것만"])

        self.sortStandardCB = QComboBox()
        self.sortStandardCBStarted = False
        self.sortStandardCB.currentIndexChanged.connect(self.sortStandardCBChanged)
        self.sortStandardCB.addItems(["저장순", "영어 오름차순", "영어 내림차순", "한글 오름차순", "한글 내림차순"])

        settingBt = self.windowsManager.qButtonMaker(
            "설정", self.buttonClicked, None, (QSizePolicy.Expanding, QSizePolicy.Expanding))

        toolbarLayout.addWidget(self.wordStandardCB, 0, 1)
        toolbarLayout.addWidget(self.sortStandardCB, 1, 1)
        toolbarLayout.addWidget(settingBt, 2, 1)


        # 단어 레이아웃. 단어들 보여줌.
        self.focusedWordHint = QCheckBox()
        self.focusedWordHint.setText("= 집중 단어")
        self.focusedWordHint.setChecked(True)
        self.focusedWordHint.setDisabled(True)

        self.wordListLayout = QVBoxLayout()
        self.wordsScrollArea = QScrollArea()
        self.wordListLayout.addWidget(self.wordsScrollArea)
        self.updateWordListUI()

        # 단어 추가 레이아웃.
        wordAddLayout = QHBoxLayout()

        wordAddLayoutLeft = QGridLayout()

        sz = (200, 90)
        self.wordAddEnTE = self.windowsManager.qTextWidgetSetter(
                QTextEdit(), "", False, Qt.AlignLeft, sz)
        self.wordAddKoTE = self.windowsManager.qTextWidgetSetter(
                QTextEdit(), "", False, Qt.AlignLeft, sz)
        wordAddLayoutLeft.addWidget(QLabel("영어"), 0, 0)
        wordAddLayoutLeft.addWidget(self.wordAddEnTE, 1, 0)
        wordAddLayoutLeft.addWidget(QLabel("한글"), 0, 1)
        wordAddLayoutLeft.addWidget(self.wordAddKoTE, 1, 1)

        wordAddLayout.addLayout(wordAddLayoutLeft)

        wordAddLayoutRight = QGridLayout()
        wordAddBt = self.windowsManager.qButtonMaker(
            "추가", self.buttonClicked, None, (QSizePolicy.Expanding, QSizePolicy.Expanding))
        wordDeleteBt = self.windowsManager.qButtonMaker(
            "삭제", self.buttonClicked, None, (QSizePolicy.Expanding, QSizePolicy.Expanding))
        wordStringClearBt = self.windowsManager.qButtonMaker(
            "취소", self.buttonClicked, None, (QSizePolicy.Expanding, QSizePolicy.Expanding))
        wordAddLayoutRight.addWidget(wordAddBt, 0, 0)
        wordAddLayoutRight.addWidget(wordDeleteBt, 2, 0)
        wordAddLayoutRight.addWidget(wordStringClearBt, 3, 0)

        wordAddLayout.addLayout(wordAddLayoutRight)
        wordAddLayout.setSizeConstraint(QLayout.SetFixedSize)


        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(toolbarLayout, 0, 0)
        mainLayout.addLayout(self.wordListLayout, 1, 0)
        mainLayout.addLayout(wordAddLayout, 2, 0)

        self.setLayout(mainLayout)
        self.setWindowTitle('Memorize Words')

    def showWindow(self):
        self.show()
        self.move(500, 100)
        pass

    def hideWindow(self):
        # self.hide()
        pass

    def wordAdd(self):
        en, ko = self.stripWordAddTextEdits()

        if en == "" and ko == "":
            return
        elif en == "":
            self.MessagingError("이름이 입력되지 않았습니다.")
            return
        elif ko == "":
            self.MessagingError("뜻이 입력되지 않았습니다.")
            return

        wordStandard = self.wordStandardCB.currentText()
        isFocused = False
        if wordStandard == "모두":
            wordStandardJudge = self.wordStandardJudgeWhoWantAll
        elif wordStandard == "집중 단어만":
            wordStandardJudge = self.wordStandardJudgeWhoWantFocused
            isFocused = True
        elif wordStandard == "집중 단어 아닌것만":
            wordStandardJudge = self.wordStandardJudgeWhoWantNotFocused
        else:
            self.MessagingError("알수 없는 오류가 발생했습니다: wordStandard에 \'" + wordStandard + "\'이 없음")
            return

        word = Word(en, ko, isFocused)
        self.windowsManager.dataManager.wordAdd(word)
        self.wordAddTextClear()
        self.updateListedWords()


    def stripWordAddTextEdits(self):
        en = self.wordAddEnTE.toPlainText().strip()
        ko = self.wordAddKoTE.toPlainText().strip()

        self.wordAddEnTE.setText(en)
        self.wordAddKoTE.setText(ko)
        return en, ko

    def wordAddTextClear(self):
        self.wordAddEnTE.clear()
        self.wordAddKoTE.clear()

    def wordDeleteButtonClicked(self):
        en, ko = self.stripWordAddTextEdits()

        enEmpty = False
        koEmpty = False

        if en == "":
            enEmpty = True
        if ko == "":
            koEmpty = True

        if enEmpty and koEmpty:
            # 아무 것도 안적은 상태라면 아무 행동도 하지 않음.
            return

        if not enEmpty and not koEmpty:
            # 둘다 적혀 있다면, 두 개가 가리키는 영단어가
            # 같은지 확인, 같다면 지우고 다르다면 에러 메시지.
            ws_en = self.findWordsAtNowListedWordsByEn(en)
            ws_ko = self.findWordsAtNowListedWordsByKo(ko)

            # 단어가 없다면 에러 메시지.
            if len(ws_en) == 0 or len(ws_ko) == 0:
                self.MessagingError("\'" + en + " " + ko + "\'는 없는 단어입니다!")
                return

            willDelete = []
            for w in ws_en:
                if w in ws_ko:
                    willDelete.append(w)
            if len(willDelete) == 0:
                self.MessagingError("단어의 이름과 뜻이 다릅니다!")
            else:
                for w in willDelete:
                    self.wordDelete(w)
        else:
            if not enEmpty:
                # 영어만 채워져 있다면, 같은 이름의 모든 단어 삭제
                ws_en = self.findWordsAtNowListedWordsByEn(en)
                if len(ws_en) == 0:
                    self.MessagingError("\'" + en + "\'이 현재 리스트에 없습니다!")
                else:
                    for w in ws_en:
                        self.wordDelete(w)
            else:
                # 한글만 채워져 있다면, 같은 뜻의 모든 단어 삭제
                ws_ko = self.findWordsAtNowListedWordsByKo(ko)
                if len(ws_ko) == 0:
                    self.MessagingError("\'" + ko + "\'이 현재 리스트에 없습니다!")
                else:
                    for w in ws_ko:
                        self.wordDelete(w)

    def wordDelete(self, word):
        en, ko = word.getStrings()
        print("Delete", en, ko)
        try:
            self.windowsManager.getNowListedWords().remove(word)
            self.windowsManager.dataManager.wordDelete(word)
            self.MessagingSuccess('\'' + en + ' ' + ko + "\'가 삭제되었습니다.")
            self.wordAddTextClear()
        except:
            self.MessagingError("없는 단어입니다.")

        self.updateListedWords()

    def MessagingSuccess(self, content):
        QMessageBox.about(self, "Success", content)

    def MessagingError(self, content):
        QMessageBox.about(self, "Error", content)

    def findWordsAtNowListedWordsByEn(self, en):
        ws = []
        for w in self.windowsManager.getNowListedWords():
            w_en, w_ko = w.getStrings()
            if w_en == en:
                ws.append(w)
        return ws

    def findWordsAtNowListedWordsByKo(self, ko):
        ws = []
        for w in self.windowsManager.getNowListedWords():
            w_en, w_ko = w.getStrings()
            if w_ko == ko:
                ws.append(w)
        return ws

    def wordStandardCBChanged(self, i):
        if not self.wordStandardCBStarted:
            self.wordStandardCBStarted = True
            return

        print("wordStandardCB current", self.wordStandardCB.currentText())
        self.updateListedWords()

    def sortStandardCBChanged(self, i):
        if not self.sortStandardCBStarted:
            self.sortStandardCBStarted = True
            return

        print("sortStandardCBChanged", i)
        self.updateListedWords()

    def updateListedWords(self):
        wordStandard = self.wordStandardCB.currentText()

        if wordStandard == "모두":
            wordStandardJudge = self.wordStandardJudgeWhoWantAll
        elif wordStandard == "집중 단어만":
            wordStandardJudge = self.wordStandardJudgeWhoWantFocused
        elif wordStandard == "집중 단어 아닌것만":
            wordStandardJudge = self.wordStandardJudgeWhoWantNotFocused
        else:
            print("wordStandard가 존재하지 않는 값입니다!:", wordStandard)
            return

        sortStandard = self.sortStandardCB.currentText()

        words = self.windowsManager.getAllWords()
        judgedWords = []
        for w in words:
            if wordStandardJudge(w):
                judgedWords.append(w)

        isReverse = False
        if sortStandard == "저장순":
            pass
        elif sortStandard == "영어 오름차순":
            judgedWords = sorted(judgedWords, key=lambda x: self.sortStandardJudgeWhoWantEn(x), reverse=False)
        elif sortStandard == "영어 내림차순":
            judgedWords = sorted(judgedWords, key=lambda x: self.sortStandardJudgeWhoWantEn(x), reverse=True)
        elif sortStandard == "한글 오름차순":
            judgedWords = sorted(judgedWords, key=lambda x: self.sortStandardJudgeWhoWantKo(x), reverse=False)
        elif sortStandard == "한글 내림차순":
            judgedWords = sorted(judgedWords, key=lambda x: self.sortStandardJudgeWhoWantKo(x), reverse=True)
        else:
            print("sortStandard가 존재하지 않는 값입니다!:", sortStandard)
            return

        self.windowsManager.setNowListedWords(judgedWords)

        self.updateWordListUI()

    def wordStandardJudgeWhoWantAll(self, word):
        return True

    def wordStandardJudgeWhoWantFocused(self, word):
        return word.getIsFocusing()

    def wordStandardJudgeWhoWantNotFocused(self, word):
        return not word.getIsFocusing()

    def sortStandardJudgeWhoWantEn(self, word):
        en, ko = word.getStrings()
        return en

    def sortStandardJudgeWhoWantKo(self, word):
        en, ko = word.getStrings()
        return ko

    def updateWordListUI(self):
        wordsLayout = QVBoxLayout()
        wordsLayout.addWidget(self.focusedWordHint)

        self.focusedCheckboxWithWord = {}

        for w in self.windowsManager.getNowListedWords():
            oneWordLayout = QHBoxLayout()

            cb = QCheckBox()
            cb.setChecked(w.getIsFocusing())

            en, ko = w.getStrings()

            wdEn = self.windowsManager.qTextWidgetSetter(
                QTextEdit(), en, True, Qt.AlignLeft, None, (QSizePolicy.Expanding, QSizePolicy.Fixed))
            wdKo = self.windowsManager.qTextWidgetSetter(
                QTextEdit(), ko, True, Qt.AlignLeft, None, (QSizePolicy.Expanding, QSizePolicy.Fixed))
            wdEn.setFixedHeight(55)
            wdKo.setFixedHeight(55)

            wdEn.selectionChanged.connect(self.wordEnClicked)
            wdKo.selectionChanged.connect(self.wordKoClicked)

            # wdEn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            # wdKo.setSizePolicy(wdEn.sizePolicy())

            cb.clicked.connect(self.focusedCheckboxClicked)
            oneWordLayout.addWidget(cb)
            oneWordLayout.addWidget(wdEn)
            oneWordLayout.addWidget(wdKo)
            wordsLayout.addLayout(oneWordLayout)

            self.focusedCheckboxWithWord[cb] = w

        wordsLayout.addStretch()

        groupBox = QGroupBox()
        groupBox.setLayout(wordsLayout)
        wordsScrollAreaNew = QScrollArea()
        wordsScrollAreaNew.setWidget(groupBox)
        wordsScrollAreaNew.setWidgetResizable(True)
        wordsScrollAreaNew.setFixedSize(550, 550)

        self.wordListLayout.replaceWidget(self.wordsScrollArea, wordsScrollAreaNew)
        self.wordsScrollArea = wordsScrollAreaNew

    def focusedCheckboxClicked(self, val):
        word = self.focusedCheckboxWithWord[self.sender()]
        en, ko = word.getStrings()
        print("Set Focused", val, en, ko)
        word.setIsFocusing(val, self.windowsManager.dataManager)
        self.updateListedWords()

    def buttonClicked(self):
        bt = self.sender().text()

        if bt == "Memorize Start":
            self.windowsManager.memorizeModeStart()
        elif bt == "추가":
            self.wordAdd()
        elif bt == "삭제":
            self.wordDeleteButtonClicked()
        elif bt == "취소":
            self.wordAddTextClear()
        elif bt == "설정":
            self.windowsManager.settingWindow.show()

    def wordEnClicked(self):
        txt = self.sender().toPlainText()
        self.wordAddEnTE.setText(txt)

    def wordKoClicked(self):
        txt = self.sender().toPlainText()
        self.wordAddKoTE.setText(txt)

    #def __del__(self):
    #    self.windowsManager.dataManager.saveAllWords()


class MemorizeWindow(QWidget):
    def __init__(self, windowsManager, parent=None):
        super().__init__(parent)
        self.windowsManager = windowsManager

        # 외울 단어들 가져오고 세팅
        self.words = self.windowsManager.getNowListedWords()[:]
        random.shuffle(self.words)
        self.nowWordIndex = 0


        # 단어 보여주는 레이아웃 세팅
        wordShowLayout = QVBoxLayout()


        topDisplayLayout = QHBoxLayout()

        self.isFocusingCheckbox = QCheckBox("집중 암기 단어")
        self.isFocusingCheckbox.clicked.connect(self.focusedCheckboxClicked)
        topDisplayLayout.addWidget(self.isFocusingCheckbox)

        topDisplayLayout.addStretch()
        self.nowProgressText = QLabel()
        topDisplayLayout.addWidget(self.nowProgressText)
        wordShowLayout.addLayout(topDisplayLayout)


        self.wordUpText = self.windowsManager.qTextWidgetSetter(
                QTextEdit(), "", True, None, None, (QSizePolicy.Expanding, QSizePolicy.Expanding), 6)
        self.wordDownText = self.windowsManager.qTextWidgetSetter(
                QTextEdit(), "", True, None, None, (QSizePolicy.Expanding, QSizePolicy.Expanding), 6)

        self.upText = ""
        self.downText = ""
        self.wordMeanShowBt = self.windowsManager.qButtonMaker(
            "", self.buttonClicked, (495, 50))
        self.isDownTextShowed = False
        self.wordDownTextHide()

        wordShowLayout.addWidget(self.wordUpText)
        wordShowLayout.addWidget(self.wordDownText)
        wordShowLayout.addWidget(self.wordMeanShowBt)

        beforeBt = self.windowsManager.qButtonMaker(
            "이전", self.buttonClicked, (150, 40))
        nextBt = self.windowsManager.qButtonMaker(
            "다음", self.buttonClicked, (150, 40))
        wordPassLayout = QHBoxLayout()
        wordPassLayout.addWidget(beforeBt)
        wordPassLayout.addStretch()
        wordPassLayout.addWidget(nextBt)

        wordShowLayout.addLayout(wordPassLayout)

        wordShowGB = QGroupBox()
        wordShowGB.setFixedSize(520, 350)
        wordShowGB.setLayout(wordShowLayout)


        # 단어 인터넷으로 검색해서 문장 가져오는 레이아웃 세팅
        self.searchWidgets = []

        self.searchWordGB = QGroupBox()
        searchWordLayout = QVBoxLayout()

        self.searchWordBt = self.windowsManager.qButtonMaker(
            "", self.buttonClicked, (500, 50))
        searchWordLayout.addWidget(self.searchWordBt)

        self.searchedMeanText = self.windowsManager.qTextWidgetSetter(
            QTextEdit(), "", True, Qt.AlignCenter, (-1, 60), (QSizePolicy.Expanding, QSizePolicy.Expanding), 3)

        sentenceTopDisplayLayout = QHBoxLayout()
        sentenceTopDisplayLayout.addStretch()
        self.nowSentenceProgressText = QLabel()
        sentenceTopDisplayLayout.addWidget(self.nowSentenceProgressText)

        self.sentenceEnText = self.windowsManager.qTextWidgetSetter(
            QTextEdit(), "", True, Qt.AlignLeft, None, (QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.sentenceKoText = self.windowsManager.qTextWidgetSetter(
            QTextEdit(), "", True, Qt.AlignLeft, None, (QSizePolicy.Expanding, QSizePolicy.Expanding))

        searchWordLayout.addWidget(self.searchedMeanText)
        self.searchWidgets.append(self.searchedMeanText)
        searchWordLayout.addLayout(sentenceTopDisplayLayout)
        self.searchWidgets.append(self.nowSentenceProgressText)
        searchWordLayout.addWidget(self.sentenceEnText)
        self.searchWidgets.append(self.sentenceEnText)
        searchWordLayout.addWidget(self.sentenceKoText)
        self.searchWidgets.append(self.sentenceKoText)

        searchWordButtonLayout = QHBoxLayout()
        sentenceBeforeBt = self.windowsManager.qButtonMaker(
            "이전 예문", self.buttonClicked, (-1, 50), (QSizePolicy.Expanding, QSizePolicy.Expanding))
        sentenceNextBt = self.windowsManager.qButtonMaker(
            "다음 예문", self.buttonClicked, (-1, 50), (QSizePolicy.Expanding, QSizePolicy.Expanding))

        searchWordButtonLayout.addWidget(sentenceBeforeBt)
        self.searchWidgets.append(sentenceBeforeBt)
        searchWordButtonLayout.addStretch()
        searchWordButtonLayout.addWidget(sentenceNextBt)
        self.searchWidgets.append(sentenceNextBt)


        searchWordLayout.addStretch()
        searchWordLayout.addLayout(searchWordButtonLayout)

        self.searchWordGB.setLayout(searchWordLayout)
        self.searchWordGB.setFixedSize(520, 450)
        self.hideSearchWord()

        self.isSearchOn = False
        self.searchedMeans = []
        self.searchedSentences = []
        self.nowSentenceIndex = 0


        self.setNowWord(0)
        # 메인 레이아웃 세팅

        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addWidget(wordShowGB, 0, 0)
        mainLayout.addWidget(self.searchWordGB, 1, 0)
        self.hideSearchWord()

        self.setLayout(mainLayout)
        self.setWindowTitle('Memorize Words')

    def showWindow(self):
        self.show()
        self.move(600, 100)
        self.activateWindow()
        pass

    def hideWindow(self):
        self.hide()
        pass

    def showSearchWord(self):
        self.searchWordBt.setText("사전 숨기기")
        for w in self.searchWidgets:
            w.show()
        self.isSearchOn = True
        self.searchAndShow()

    def hideSearchWord(self):
        self.searchWordBt.setText("사전 보이기")
        for w in self.searchWidgets:
            w.hide()
        self.isSearchOn = False

    def buttonClicked(self):
        btbt = self.sender()
        bt = btbt.text()

        if bt == "이전":
            self.setNowWord(-1)
        if bt == "다음":
            self.setNowWord(1)
        elif bt == "뜻 숨기기":
            self.wordDownTextHide()
        elif bt == "뜻 보이기":
            self.wordDownTextShow()
        elif bt == "사전 보이기":
            self.showSearchWord()
        elif bt == "사전 숨기기":
            self.hideSearchWord()
        elif bt == "다음 예문":
            if self.nowSentenceIndex < len(self.searchedSentences) -1:
                self.setNowSentence(1)
        elif bt == "이전 예문":
            if self.nowSentenceIndex > 0:
                self.setNowSentence(-1)

    def setNowWord(self, i):
        self.nowWordIndex += i

        if self.nowWordIndex < 0:
            self.nowWordIndex = 0
        elif self.nowWordIndex >= len(self.words):
            self.nowWordIndex = len(self.words) - 1

        nowWord = self.words[self.nowWordIndex]
        self.isFocusingCheckbox.setChecked(nowWord.getIsFocusing())

        en, ko = nowWord.getStrings()
        self.upText = en
        self.wordUpText.setText(self.upText)
        self.wordUpText.setAlignment(Qt.AlignCenter)
        self.downText = ko
        if self.isDownTextShowed:
            self.wordDownTextShow()
        else:
            self.wordDownTextHide()

        if self.isSearchOn:
            self.searchAndShow()

        self.nowProgressText.setText(str(self.nowWordIndex + 1) + " / " + str(len(self.words)))

    def searchAndShow(self):
        connection, means, sentences = self.windowsManager.webCrawler.searchEnglish(self.upText)

        self.searchedMeans = means
        self.searchedSentences = sentences

        if len(self.searchedMeans) == 0:
            self.searchedMeanText.clear()
        else:
            joined = ", ".join(self.searchedMeans)
            self.searchedMeanText.setText(joined)
            self.searchedMeanText.setAlignment(Qt.AlignCenter)

        self.nowSentenceIndex = 0
        self.setNowSentence(0)

    def setNowSentence(self, i):
        self.nowSentenceIndex += i
        searchedSentences_len = len(self.searchedSentences)

        if self.nowSentenceIndex > searchedSentences_len - 1:
            self.nowSentenceIndex = searchedSentences_len - 1
        elif self.nowSentenceIndex < 0:
            self.nowSentenceIndex = 0

        self.nowSentenceProgressText.setText("예문   " + str(self.nowSentenceIndex + 1) + " / " + str(searchedSentences_len))

        if searchedSentences_len == 0:
            self.sentenceEnText.clear()
            self.sentenceKoText.clear()
        else:
            self.sentenceEnText.setText(self.searchedSentences[self.nowSentenceIndex][0])
            self.sentenceKoText.setText(self.searchedSentences[self.nowSentenceIndex][1])

    def wordDownTextShow(self):
        self.wordDownText.setText(self.downText)
        self.wordDownText.setAlignment(Qt.AlignCenter)
        self.wordMeanShowBt.setText("뜻 숨기기")
        self.isDownTextShowed = True

    def wordDownTextHide(self):
        self.wordDownText.clear()
        self.wordMeanShowBt.setText("뜻 보이기")
        self.isDownTextShowed = False

    def focusedCheckboxClicked(self, val):
        self.words[self.nowWordIndex].setIsFocusing(val, self.windowsManager.dataManager)
        self.windowsManager.mainWindow.updateListedWords()


class SettingWindow(QWidget):
    def __init__(self, windowsManager, parent=None):
        super().__init__(parent)
        self.windowsManager = windowsManager

        aGroup = QGroupBox("알림 발행 토픽")
        aBox = QHBoxLayout()
        self.topicSettingText = self.windowsManager.qTextWidgetSetter(
            QLineEdit(), "", False
        )
        aBox.addWidget(self.topicSettingText)
        aGroup.setLayout(aBox)

        '''
        bGroup = QGroupBox("방해 금지 시간")
        bBox = QHBoxLayout()
        self.dontPushStart = QTimeEdit()
        bBox.addWidget(self.dontPushStart)
        bBox.addWidget(QLabel("부터 "))
        self.dontPushEnd = QTimeEdit()
        bBox.addWidget(self.dontPushEnd)
        bBox.addWidget(QLabel("까지"))
        bGroup.setLayout(bBox)
        '''

        cGroup = QGroupBox("푸시 알림 간격")
        cBox = QHBoxLayout()
        self.pushIntervalStart = QLineEdit()
        cBox.addWidget(self.pushIntervalStart)
        cBox.addWidget(QLabel("분 부터 "))
        self.pushIntervalEnd = QLineEdit()
        cBox.addWidget(self.pushIntervalEnd)
        cBox.addWidget(QLabel("분 사이"))
        cGroup.setLayout(cBox)

        # 메인 레이아웃 세팅
        mainLayout = QVBoxLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addWidget(aGroup)
        # mainLayout.addWidget(bGroup)
        mainLayout.addWidget(cGroup)

        bt = self.windowsManager.qButtonMaker(
            "설정 저장", self.buttonClicked, (-1, 50), (QSizePolicy.Expanding, QSizePolicy.Expanding)
        )
        mainLayout.addWidget(bt)

        self.setLayout(mainLayout)
        self.setWindowTitle('Memorize Words')

    def buttonClicked(self):
        bt = self.sender().text()

        if bt == "설정 저장":
            # print(self.dontPushEnd.time().hour(), self.dontPushEnd.time().minute())
            self.settingApplyAndSave()
            pass

    def settingApplyAndSave(self):
        self.windowsManager.pushSender.word_send_topic = self.topicSettingText.text()

        pushintervalstart = int(self.pushIntervalStart.text())
        pushintervalend = int(self.pushIntervalEnd.text())

        self.windowsManager.pushSender.setWaitTime(pushintervalstart, pushintervalend)

        # st_h = self.dontPushStart.time().hour()
        # st_m = self.dontPushStart.time().minute()
        # ed_h = self.dontPushEnd.time().hour()
        # ed_m = self.dontPushEnd.time().minute()
        # sted = [(st_h, st_m), (ed_h, ed_m)]
        # self.windowsManager.pushSender.setDontTime(sted)

        # self.dontPushStart.setTime()

        sts = []
        sts.append(self.topicSettingText.text())
        sts.append((pushintervalstart, pushintervalend))
        # sts.append(sted)
        sts.append([(0, 0), (0, 0)])

        self.windowsManager.dataManager.saveAllSettings(sts)

        self.hide()

    def settingLoad(self, sts):
        self.topicSettingText.setText(sts[0])

        self.pushIntervalStart.setText(str(sts[1][0]))
        self.pushIntervalEnd.setText(str(sts[1][1]))

        '''
        sss = sts[2]
        st_h = sss[0][0]
        st_m = sss[0][1]
        ed_h = sss[1][0]
        ed_m = sss[1][1]
       
        self.dontPushStart.setHM(st_h, st_m, 0)
        self.dontPushEnd.setHM(ed_h, ed_m, 0)
        '''
        self.settingApplyAndSave()



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    manager = WindowsManager(True)
    sys.exit(app.exec_())