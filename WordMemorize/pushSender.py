
import time
import threading
import random
import json
import requests

from word import Word

class PushSender:
    def __init__(self, dataManager, topic):
        self.key = 'AAAACPx03Kk:APA91bH5xqtWB23DRQdMwGUQkUc7HFlHV8qd3xmNeZkxbyJ1WgKXKR9u9Y3aEPe9_3pJJgT3v0HR2QGNhi1FjZXQ3_aq4LRC_oIpmVznieg2GHeKgED9R3HkFC0D89VsPjK6bBS8H-tT'
        self._word_send_topic = topic
        self.pushsending_stop = False
        self.dataManager = dataManager

        self.setWaitTime(1, 2)

    def setWaitTime(self, min_time, max_time):
        self.waitTimeMin = min_time * 60

        self.waitTimeMax = max_time * 60

        if self.waitTimeMax <= self.waitTimeMin:
            self.waitTimeMax = self.waitTimeMin + 1


    @property
    def word_send_topic(self):
        return self._word_send_topic

    @word_send_topic.setter
    def word_send_topic(self, topic):
        self._word_send_topic = topic


    def pushSend(self, word):
        en, ko = word.getStrings()
        self.sendFcmNotification(en, self.word_send_topic, ko)

    def sendFcmNotification(self, title, topic, body):
        # fcm 푸시 메세지 요청 주소
        url = 'https://fcm.googleapis.com/fcm/send'

        # 인증 정보(서버 키)를 헤더에 담아 전달
        headers = {
            'Authorization': 'key=' + self.key,
            'Content-Type': 'application/json; UTF-8',
        }

        # 보낼 내용과 대상을 지정
        content = {
            'notification': {
                'title': title,
                'body': body
            },
            'to': '/topics/' + topic,
            'priority': 'high',
            'data': {
                'title': title,
                'message': body
            }
        }

        # json 파싱 후 requests 모듈로 FCM 서버에 요청
        try:
            requests.post(url, data=json.dumps(content), headers=headers)
            print("Sended:", title, body, "to", topic)
        except:
            print("Send Failed. 인터넷 연결을 확인하세요.")

    def pushsendingDaemon(self):
        print('Push sending started.')
        foc_words = []

        while True:
            waittime = random.randrange(self.waitTimeMin, self.waitTimeMax)
            time.sleep(waittime)

            if self.pushsending_stop:
                break

            if len(foc_words) == 0:
                foc_words = self.dataManager.getFocusedWords()[:]

            if len(foc_words) != 0: # 애초에 getFocusedWords에서 빈 리스트가 올 수도 있으므로
                self.pushSend(foc_words.pop(random.randrange(0, len(foc_words))))

        print('Push sending ended.')

    def pushSendingThreadStart(self):
        self.pushsending_stop = False

        self.pushsending_daemon = threading.Thread(target=self.pushsendingDaemon, args=())
        self.pushsending_daemon.daemon = True
        self.pushsending_daemon.start()

    def pushSendingThreadEnd(self):
        self.pushsending_stop = True


