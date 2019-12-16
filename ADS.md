# 소프트웨어 구조 설계서 (ADS)

# 모듈 및 클래스 설계
## module word.py
### class Word
단어의 정보가 저장되는 클래스이다. 단어를 하나의 객체로 보기 위해 클래스로 선언한다.


## module main.py
### class WindowsManager
다양한 윈도우들을 통합적으로 관리하는 클래스이다. 처음 프로그램이 실행되면 나오는 단어 리스트 윈도우, 그리고 암기 모드로 들어가면 나오는 단어 암기 윈도우 총 두 개의 윈도우를 동작하거나 동작하지 않게 제어한다. 또한 WindowsManager이 가지고 있는 다른 클래스 객체에게 메시지를 전달하거나 값을 받아와야 할 때 두 윈도우가 필요로 하는 메서드를 제공해준다.

### class MainWindow(QWidget)
처음 프로그램이 실행되면 나오는 단어 리스트 윈도우의 역할을 담당하는 클래스이다. QWidget 클래스를 상속한다. 단어 리스트 윈도우의 버튼 눌림을 처리하고, GUI 요소를 관리하는 등 단어 리스트 윈도우 내의 동작을 총괄한다.

### class MemorizeWindow(QWidget)
단어 암기 윈도우의 역할을 담당하는 클래스이다. QWidget 클래스를 상속한다. 단어 암기 윈도우의 버튼 눌림을 처리하고, GUI 요소를 관리하는 등 단어 암기 윈도우 내의 동작을 총괄한다.


## module dataManager.py
### class DataManager
데이터를 읽고 저장하는 역할을 하는 클래스이다. 단어들의 정보를 텍스트로 저장하거나 텍스트 파일에서 단어들을 읽어올 수 있다.

## module webCrawler.py
### class WebCrawler
웹 크롤링을 통해 인터넷에서 단어의 정보를 불러오고 필요한 정보를 걸러내는 역할을 하는 클래스이다. 영단어의 인터넷 사전상 뜻과 해당 단어가 쓰인 예문, 예문의 뜻을 가져온다.


## module pushSender.py
### class PushSender
안드로이드 스마트폰에 푸시 알림을 보내는 역할을 하는 클래스이다. Firebase 서버에 http 요청을 하여 특정한 스마트폰에 알림이 갈 수 있도록 한다.


# 클래스별 메서드 설계
## module word.py
```python3
class Word:
    def __init__(self, en, ko, foc):
        # 주어진 입력으로 이 단어의 영문자와 한글뜻, 그리고 이 단어가 '집중 암기'인지 설정한다.

    def getStrings(self):
        # 단어의 영문자, 한글뜻 정보를 한 번에 불러온다.
        return self.en, self.ko

    def getIsFocusing(self):
        # 단어가 '집중 암기' 단어인지 리턴한다.
        return self.isFocusing

    def setIsFocusing(self, foc):
        # 주어진 입력으로, 이 단어가 '집중 암기' 단어인지 아닌지를 재설정한다.
```

## module main.py
```python3
class WindowsManager:
    def __init__(self):
        # 프로그램에 쓰일 객체들
        # (MainWindow, MemorizeWindow, WebCrawler, DataManager, PushSender)
        # 을 생성하고 세팅한다.

    def memorizeModeStart(self):
        # 암기 모드를 시작한다.

    def memorizeModeEnd(self):
        # 암기 모드를 종료한다.
```

```python3
class MainWindow(QWidget):
    def __init__(self):
        # 메인 윈도우(단어 리스트 윈도우)의 GUI 요소를 세팅한다.

    def showWindow()
        # 이 윈도우, 즉 메인 윈도우 창이 나오게 한다.
        
    def hideWindow()
        # 이 윈도우, 즉 메인 윈도우 창이 사라지게 한다.
        
    def wordAdd()
        # 단어 리스트에 새로운 단어를 추가한다.
        
    def wordDelete(word)
        # 단어 리스트에 있는 단어 중 word에 해당하는 단어를 삭제한다.
        
    def updateListedWords():
        # 현재 화면에 나타난 단어 목록을 재설정한다.
        
    def buttonClicked():
        # 버튼 눌림을 처리한다.
```

```python3
class MemorizeWindow(QWidget):
    def __init__(self):
        # 단어 암기 윈도우의 GUI 요소를 세팅한다.

    def showWindow()
        # 이 윈도우, 즉 단어 암기 윈도우 창이 나오게 한다.
        
    def hideWindow()
        # 이 윈도우, 즉 단어 암기 윈도우 창이 사라지게 한다.
        
    def showSearchWord(self):
        # 인터넷에서 단어의 정보를 불러온 결과를 나타내는 레이아웃을 보이게 한다.

    def hideSearchWord(self):
        # 인터넷에서 단어의 정보를 불러온 결과를 나타내는 레이아웃을 숨긴다.

    def buttonClicked(self):
        # 버튼 눌림을 처리한다.  

    def setNowWord(self, i):
        # 지금 보여줄 단어를 설정한다.

    def wordDownTextShow(self):
        # 단어 뜻을 보이게 한다.

    def wordDownTextHide(self):
        # 단어 뜻을 숨긴다.
```

## module dataManager.py
```python3
class DataManager:
    def __init__(self):
        # 변수 초기 설정을 하고, 단어 정보를 불러온다.

    def readAllWords(self):
        # 파일에서 모든 단어의 정보를 읽어온다.

    def saveAllWords(self):
        # 파일에 모든 단어의 정보를 저장한다.
```

## module webCrawler.py
```python3
class WebCrawler:
    def __init__(self):
        # 변수 초기 설정을 한다.

    def searchEnglish(self, en):
        # 주어진 인자에 해당하는 단어를 검색하고,
        # 웹 크롤링을 통해 정보를 받아온 후 필요한 것만 걸러낸다.
        # 정복가 잘 불러와졌는지, 단어의 인터넷 사전상 뜻은 무엇인지,
        # 인터넷 사전에 등록된 해당 단어의 예문과 그 뜻에는 무엇이 있는지를 리턴한다.
        return connection, means, sentences
```

## module pushSender.py
```python3
class PushSender:
    def __init__(self):
        # 변수 초기 설정을 한다.

    def pushSend(word, topic)
        # firebase 기반으로, 제목은 word의 영어, 내용은 word의 한글인
        # 푸시 알림을 topic 토픽으로 보낸다.
        # 해당 토픽을 구독하고 있는 앱으로 알림이 가게 된다.
        
    def pushSendingThreadStart(self):
        # 지속적으로 푸시 알림을 보내는 쓰레드를 실행한다.
        
    def pushSendingThreadEnd(self):
        # 지속적으로 푸시 알림을 보내는 쓰레드를 종료한다.
```

# 클래스별 상호작용

