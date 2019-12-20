import re
from urllib import request
from bs4 import BeautifulSoup

def craete_soup_with_url(url):
    handler = request.urlopen(url)
    source = handler.read().decode('utf-8')
    return BeautifulSoup(source, 'html.parser')

def create_soup_with_query(query):
    url = 'http://dic.daum.net/search.do?dic=eng&q=' + query
    return craete_soup_with_url(url)


def create_soup_with_wordid(wordid):
    url = 'http://dic.daum.net/word/view.do?wordid=' + wordid
    return craete_soup_with_url(url)


def get_word_id(url):
    return re.findall('ekw[\d]+', url)[0]


def get_meaning_words(query):
    soup = create_soup_with_query(query)
    refresh_meta = soup.find('meta', attrs={'http-equiv': 'Refresh'})

    if refresh_meta is not None:
        wordid = get_word_id(refresh_meta.get('content'))
        soup = create_soup_with_wordid(wordid)

    final_page_anchor = soup.find('a', property='og:description')  # first link_word

    if final_page_anchor is not None:
        wordid = get_word_id(final_page_anchor.get('href'))
        soup = create_soup_with_wordid(wordid)

    meaning_words = []
    meaning_div = None
    for tag in soup.find_all("meta"):
        if tag.get("property", None) == 'og:description':
            meaning_div = tag.get('content', None)

    if meaning_div is not None:
        meaning_words = [meaning_div]
        meaning_words = [w.strip() for w in meaning_words]
        meaning_words = [w for w in meaning_words if w != '']

    paragraph_data_all = soup.find_all('span', class_='txt_example')
    # paragraph_data_all은 예문 영어를 불러온다.
    paragraph_data_all_2 = soup.find_all('a', class_='link_example link_example2')
    paragraph_data_all_2_len = len(paragraph_data_all_2)
    # paragraph_data_all_2는 예문 맨 끝에 출처가 담긴 부분을 불러온다.
    # paragraph_data_all에서 불러온 예문에 출처가 포함되는데,
    # 이것을 지우기 위해 출처를 따로 불러온 것이다.
    paragraph_data_means = soup.find_all('span', class_='mean_example')
    paragraph_data_means_len = len(paragraph_data_means)
    # paragraph_data_means는 예문 한글을 불러온다.

    sentences = []

    for i in range(len(paragraph_data_all)):
        paragraph_data = paragraph_data_all[i]
        getted = paragraph_data.get_text()
        getted_sp = getted.split('\n')
        # getted는 하나의 문자열이지만, \n로 줄이 나뉘어져 있다.
        # 그런데 필요로 하는 문장은 한 줄에만 담겨있고, 다른 줄은 필요 없는 정보들이다.
        # 원하는 줄만 불러올 수 있도록 \n을 기준으로 문자열을 나눈다.

        sentence = NoNullReturn(getted_sp)

        if paragraph_data_all_2_len > i:
            paragraph_data2 = paragraph_data_all_2[i]
            willDelete = paragraph_data2.get_text()
            sentence = sentence.replace(willDelete, "")
            # 출처 지우기 작업.

        sentence_mean = ""
        if paragraph_data_means_len > i:
            paragraph_data_mean = paragraph_data_means[i]
            sentence_mean = NoNullReturn(paragraph_data_mean.get_text().split('\n'))

        sentences.append((sentence, sentence_mean))

    return meaning_words, sentences

def NoNullReturn(lst):
    # 예문 영어나 예문 한글을 불러올 때,
    # 첫 줄에 빈 줄이 들어간 경우도 있고, 바로 예문이 나오는 경우도 있어서
    # 비지 않은 줄 부분을 탐지해 리턴하도록 하는 함수이다.
    for s in lst:
        if s.strip() != "":
            return s
    else:
        return lst[0]



if __name__ == '__main__':
    meaning_words, sentences = get_meaning_words("hello")
    print(sentences)
    meaning_words, sentences = get_meaning_words("qwer")
    print(sentences)