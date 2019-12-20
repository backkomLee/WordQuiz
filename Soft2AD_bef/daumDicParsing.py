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

    paragraph_data_all = soup.find_all('span', class_='txt_example')
    paragraph_data_all_2 = soup.find_all('a', class_='link_example link_example2')
    paragraph_data_all_2_len = len(paragraph_data_all_2)
    paragraph_data_means = soup.find_all('span', class_='mean_example')
    paragraph_data_means_len = len(paragraph_data_means)

    sentences = []

    for i in range(len(paragraph_data_all)):
        paragraph_data = paragraph_data_all[i]
        # print(paragraph_data)
        getted = paragraph_data.get_text()
        # print(getted)
        getted_sp = getted.split('\n')

        sentence = NoNullReturn(getted_sp)

        if paragraph_data_all_2_len > i:
            paragraph_data2 = paragraph_data_all_2[i]
            willDelete = paragraph_data2.get_text()
            # print("O:", willDelete)
            sentence = sentence.replace(willDelete, "")

        sentence_mean = ""
        if paragraph_data_means_len > i:
            paragraph_data_mean = paragraph_data_means[i]
            sentence_mean = NoNullReturn(paragraph_data_mean.get_text().split('\n'))

        # print("A:", sentence)
        # print("B:", sentence_mean)
        sentences.append((sentence, sentence_mean))

    meaning_div = None
    for tag in soup.find_all("meta"):
        if tag.get("property", None) == 'og:description':
            meaning_div = tag.get('content', None)

    if meaning_div is not None:
        # meaning_words = re.split('[1.-9.]', meaning_div)
        meaning_words = [meaning_div]
        meaning_words = [w.strip() for w in meaning_words]
        meaning_words = [w for w in meaning_words if w != '']

    return meaning_words, sentences

def NoNullReturn(lst):
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