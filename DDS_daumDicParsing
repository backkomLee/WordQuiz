# 소프트웨어 상세 설계서 (DDS)

## daumDicParsing.py
### class WebCrawler

```python3
import re
from urllib import request
from bs4 import BeautifulSoup
```

```python3
def craete_soup_with_url(url):
    # request.urlopen으로 정보를 가져온다.
    # 이를 utf-8로 디코드하고,
    # BeautifulSoup 객체를 만들어 리턴한다.

def create_soup_with_query(query):
    # 쿼리 기반 링크로 데이터를 가져온다.
    # url 생성 후 craete_soup_with_url

def create_soup_with_wordid(wordid):
    # 단어의 id 기반 링크로 데이터를 가져온다.
    # url 생성 후 craete_soup_with_url
    
def get_word_id(url):
    # url에서 re.findall을 이용해 단어의 id 부분을 따오고, 이를 리턴한다.
```

```python3
def get_meaning_words(query):
    # create_soup_with_query을 통해 데이터를 받아오고,
    # BeautifulSoup 객체의 find 메서드를 이용해 이를 단어 뜻과 문장을 받아오기 좋은 형태로 가공한다.
    # 단어가 한 번에 검색되지 않고, 검색했을 때 여러 단어가 리스트로 나오는 화면이 나온다면
    # 그 안에서 상단의 단어를 선택하여 들어가고, 그곳의 데이터를 받아와 정제한다.
    
    # 정제한 데이터에서 property가 og:description인 부분의 데이터에서 content 부분을 받아온다.
    # 이것을 처리하면 단어의 뜻이 나온다. 이를 string의 list 형태로 meaning_words에 담는다.
    

    # paragraph_data_all = 예문 영어 데이터 부분을 불러와서 저장한다.
    
    # paragraph_data_all_2 = 예문 맨 끝에 출처가 담긴 부분을 불러와서 저장한다.
    # paragraph_data_all에서 불러온 예문에 출처가 포함되는데,
    # 이것을 지우기 위해 출처를 따로 불러온 것이다.
    
    # paragraph_data_means = 예문 한글 데이터 부분을 불러와서 저장한다.

    sentences = []

    paragraph_data_all = # soup.find_all을 통해 예문 영어가 포함된 클래스들의 데이터를 모두 가져온다.
    paragraph_data_all_2 = # soup.find_all을 통해 각각의 예문의 출처가 포함된 클래스들의 데이터를 모두 가져온다. 
    # paragraph_data_all에 예문 출처가 섞여서 들어오기 때문에, 출처 부분만 따로 걸러내기 위해 한번 더 검색하는 것이다.
    paragraph_data_means = # soup.find_all을 통해 예문 한국어가 포함된 클래스들의 데이터를 모두 가져온다.

    sentences = # 예문들의 영어, 한글을 담은 튜플을 담는 리스트.

    # paragraph_data_all 리스트의 원소를 하나하나 돌아가며 get_text() 메서드를 통해 문장을 추출한다.
    # 그런데 여러 줄의 문자열이 리턴되고, 그 중 필요한 데이터(문장)은 단 한 줄에만 있으므로,
    # '\n'을 기준으로 문자열을 split한 후 NoNullReturn함수를 통해 문장 데이터를 가져온다.
    # 가져온 값을 sentence 변수에 저장한다.

    # paragraph_data2_all의 같은 index의 원소에 대해서도 같은 추출 알고리즘으로 출처를 가져온다. 
    # 그리고 가져온 출처와 같은 문자열을 sentence 변수에서 지운다.

    # paragraph_data_means의 같은 index의 원소에 대해서도 같은 추출 알고리즘으로 한글 문장을 가져오고,
    # 이를 sentence_mean 변수에 저장한다.

    # 이후 sentences에 sentence와 sentence_mean을 묶은 튜플을 append한다.

    # 반복이 끝나면 meaning_words와 sentences를 리턴한다.
```

```python3
def NoNullReturn(lst):
    # lst는 sting의 리스트이다.
    # lst의 원소 중 처음으로 나오는 '비지 않은 부분' 탐지해 리턴하도록 한다.
    # '비었다'는 문자열이 ""임을 의미한다.
```
