# 소프트웨어 상세 설계서 (DDS)

## pushSender.py
### class PushSender
```python3
    def __init__(self, (DataManager)dataManager, (string)topic):
        (string) self.key
        ->  파이어베이스 API 키가 저장되는 변수이다.
        
        (string)self._word_send_topic = topic
        ->  FCM으로 메시지를 보낼 토픽을 저장하는 변수이다.
            메시지를 보내면 앱 설치자 중 해당 토픽을 '구독'하고있는 사용자에게 푸시 알림이 가게 된다.
        
        (boolean)self.pushsending_stop = False
        ->  푸시 알림을 지속적으로 보내는 쓰레드를 종료하기 위한 변수.
            변수의 값을 True로 바꾸면 쓰레드에서 이를 감지하고,
            무한 루프를 스스로 끊는다.
        
        (DataManager)self.dataManager = dataManager
        ->  DataManager 객체에게서 푸시 알림을 보낼 단어들의 리스트를 받아야 하므로
            변수를 선언하여 언제든 '집중 단어 리스트'를 불러올 수 있도록 한다.

        self.setWaitTime((int), (int))
        ->  
        
        빨강은 문법 오류에 쳐지는 것인가?
        *&^%!...;;..;.
        kkkk === 1 !+!+ 1
```
