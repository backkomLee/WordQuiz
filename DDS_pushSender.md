# 소프트웨어 상세 설계서 (DDS)

## pushSender.py
### class PushSender

```ptrhon3
import time
import threading
import random
import json
import requests

from word import Word
```

```python3
    def __init__(self, (DataManager)dataManager, (string)topic):
        # dataManager은 WindowsManager가 생성한 DataManager 객체를 받아온다.
        
        (string)self.key
        # 파이어베이스 API 키가 저장되는 변수이다.
        
        (string)self._word_send_topic = topic
        # FCM으로 메시지를 보낼 토픽을 저장하는 변수이다.
        # 메시지를 보내면 앱 설치자 중 해당 토픽을 '구독'하고있는 사용자에게 푸시 알림이 가게 된다.
        
        (boolean)self.pushsending_stop = False
        # 푸시 알림을 지속적으로 보내는 쓰레드를 종료하기 위한 변수.
        # 변수의 값을 True로 바꾸면 쓰레드에서 이를 감지하고,
        # 무한 루프를 스스로 끊는다.
        
        (DataManager)self.dataManager = dataManager
        # DataManager 객체에게서 푸시 알림을 보낼 단어들의 리스트를 받아야 하므로
        # 변수를 선언하여 언제든 '집중 단어 리스트'를 불러올 수 있도록 한다.

        self.setWaitTime((int), (int))
        # 푸시 알림을 보내는 쓰레드에서 '알림 시간 간격'을 확인할 수 있도록
        # 두 self 변수 (int)self.waitTimeMin과 (int)self.waitTimeMax를 생성하고 값을 초기화한다.
```

```python3
    def setWaitTime(self, (int)min_time, (int)max_time):
        # min_time과 max_time은 분 기준으로 값을 받아온다.
        
        (int)self.waitTimeMin = min_time * 60
        (int)self.waitTimeMax = max_time * 60
        # time.sleep은 초 단위로 행해지므로, 60을 곱해
        
        # waitTimeMax이 waitTimeMin와 같거나 작은 상황에 대해 처리해야 한다.
        # waitTimeMax의 값을 waitTimeMin에 1을 더한 값으로 정하도록 한다.
```

```python3
    @property
    def word_send_topic(self):
        return self._word_send_topic

    @word_send_topic.setter
    def word_send_topic(self, topic):
        self._word_send_topic = topic
```

```python3
    @property
    def word_send_topic(self):
        return self._word_send_topic

    @word_send_topic.setter
    def word_send_topic(self, topic):
        self._word_send_topic = topic
        # 나중에 _word_send_topic의 값을 설정할 때 행해야 할
        # 작업이 추가된다면, 여기에 필요한 코드를 추가한다.
```

```python3
    def pushSend(self, word):
        # word에게서 해당 단어의 이름과 뜻을 불러오고 변수에 저장한다.
        # 불러온 값과 self.word_send_topic을 기반으로
        # self.sendFcmNotification 메서드를 호출하여 푸시 알림을 보낸다.
```

```python3
    def sendFcmNotification(self, title, topic, body):
        url = 'https://fcm.googleapis.com/fcm/send'
         # fcm 푸시 메세지를 요청할 주소이다.

        # headers 변수에 FCM 서버가 요구하는 형식으로 헤더를 담는다.
        # 컨텐츠 타입은 UTF-8 인코딩의 json 타입으로,
        # 인증은 self.key에 저장된 서버 키 값으로 한다.

        # content 변수에 서버에 요청을 보내면서 전달할 값을 저장한다.
        # FCM 서버가 요구하는 사항을 만족시키면서,
        # 푸시 알림의 타이틀에는 title이, 내용에넌 body가 들어가도록 한다.

        # content를 json 파싱한다.
        # requests.post의 url, content, headers값을 넣어 FCM 서버에 푸시 알림을 요청
        # 인터넷 연결이 되어있지 않은 상황에 대해 예외 처리를 한다.
```

```python3
    def pushsendingDaemon(self):
        print('Push sending started.')
        foc_words = []
        # 집중 암기 단어들을 집어넣는 리스트이다.
        # 단어가 중복되어서 알림이 보내지지 않도록 하기 위해
        # 이 리스트가 비워질 때까지 푸시 알림을 보내고,
        # 비워지면 다시 원래의 집중 암기 리스트로 초기화한다.

        while True:
            # self.waitTimeMin과 self.waitTimeMax 사이만큼 기다린다.

            if self.pushsending_stop:
                break
                # 쓰레드를 중간에 종료해야 한다면 종료한다.

            # 만약 foc_words가 비었다면 dataManager에게서 fucusedWords를 받아온다.
            
            # foc_words가 비어있지 않다면,
            # foc_words에서 랜덤으로 한 원소를 pop하여,
            # 이 원소를 인자로 pushSend 메서드를 호출한다.
```

```python3
    def pushSendingThreadStart(self):
        self.pushsending_stop = False

        # pushsendingDaemon 메서드를 '데몬 쓰레드'로 실행한다.
        
    def pushSendingThreadEnd(self):
        self.pushsending_stop = True
```


        
        
        

