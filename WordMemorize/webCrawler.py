from daumDicParsing import *

class WebCrawler:
    def __init__(self):
        pass

    def searchEnglish(self, en):
        connection = True

        try:
            means, sentences = get_meaning_words(en)
        except:
            means, sentences = [], []
            connection = False

        return connection, means, sentences
