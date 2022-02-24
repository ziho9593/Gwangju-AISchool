# 더 쉽게 복사해서 하는등의 방법이 있지만, 기본 구조를 이해하기 위해서 하나씩 차근차근 진행해보았습니다 !
# 다른 여러 방법으로 해보셔도 좋아요 :)

import requests, csv
from bs4 import BeautifulSoup, NavigableString, Tag

# base_url = 'https://search.naver.com/search.naver?&where=news&query=%EA%B4%91%EC%A3%BC%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=69&start='
# start_num = 1
# end_url = '&refresh_start=0'

# URL = base_url + str(start_num) + end_url

# response = requests.get(URL)
# soup = BeautifulSoup(response.text, 'html.parser')



# # select()를 사용하면 모든 결과를 리스트에 담고, select_one()을 사용하면 하나의 요소만 반환
# news_section = soup.select_one(
#     'div[id=wrap] > div[id=container] > div[id=content] > div[id=main_pack] > div.news.mynews.section._prs_nws > ul[class=type01] > li')

# # select_one은 NavigableString이라 반복을 돌 수 없다.
# for news in news_section:
#     if isinstance(news, NavigableString):
#         continue
#     if isinstance(news, Tag):
#          print(news.select_one('dl > dt > a')['title'])
#     print(news.select_one('dl > dt > a')['href'], '\n')

# # select는 반복문 사용 가능
# news_section = soup.select(
#     'div[id=wrap] > div[id=container] > div[id=content] > div[id=main_pack] > div.news.mynews.section._prs_nws > ul[class=type01] > li')

# for news in news_section:
#     a_tag = news.select_one('dl > dt > a')
#     print(news.select_one('dl > dt > a')['title'])
#     print(news.select_one('dl > dt > a')['href'], '\n')


# 반복문을 사용해 원하는 만큼의 데이터를 추출 (각 페이지의 정보를 배열에 담는다)
soup_objects = []

base_url = 'https://search.naver.com/search.naver?&where=news&query=광주 인공지능 사관학교&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=69&start='
end_url = '&refresh_start=0'

for i in range(1, 102, 10):
    start_num = i    

    URL = base_url + str(start_num) + end_url

    response = requests.get(URL)

    soup = BeautifulSoup(response.text, 'html.parser')
    soup_objects.append(soup)

# print(len(soup_objects))

# 실습 : soup_object에 여러 개 닮겨 있는 배열을 하나씩 선택해야하는 상황 (반복문)
for soup in soup_objects:
    news_section = soup.select(
        'div[id=wrap] > div[id=container] > div[id=content] > div[id=main_pack] > div.news.mynews.section._prs_nws > ul[class=type01] > li')

    for news in news_section:
        a_tag = news.select_one('dl > dt > a')
        news_title = a_tag['title']
        news_link = a_tag['href']
        # print(news_title)
        # print(news_link, '\n')

        news_data = {
            "title": news_title,
            "hyperlink": news_link
        }

        # csv 파일 업로드
        with open('./naver_news.csv', 'a', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'hyperlink']
            csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csvwriter.writerow(news_data)