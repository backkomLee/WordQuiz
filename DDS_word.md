# 소프트웨어 상세 설계서 (DDS)

## word.py
### class Word

```python3
    def __init__(self, en, ko, foc):
        self.en = en
        self.ko = ko
        
        self.isFocusing = foc
        # 단어가 '집중 암기 단어'인지 저장하는 변수이다.

    def getStrings(self):
        # 단어를 이용할 때는 대부분 영어와 한글 모두를 필요로 한다
        # 하나의 메서드로 한 번에 불러올 수 있도록 한다.
        return self.en, self.ko

    def getIsFocusing(self):
        return self.isFocusing

    def setIsFocusing(self, foc, dataManager):
        self.isFocusing = foc

        dataManager.saveAllWords()
        # 정보가 바뀌었으므로, DataManager 객체가 바뀐 상태를 저장하게 한다.
```
