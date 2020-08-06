import requests
from bs4 import BeautifulSoup

movie_code_response = requests.get('https://movie.naver.com/movie/running/current.nhn')
movie_code_soup = BeautifulSoup(movie_code_response.text, 'html.parser')

movies = []
movie_list = movie_code_soup.select(
    # '#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li'
    '#content > .article > .obj_section > .lst_wrap > ul > li')

for movie in movie_list:   
    a_tag = movie.select_one('dl > dt > a')
    
    title = a_tag.text
    # title = a_tag.contents[0]
    
    link = a_tag['href']
    code = link.split('code=')[1]
    # split 사용하지 않고 가져오기
    # code = link[link.find('code=') + len('code='):]
    
    movie_data = {
        "title": title,
        "code": code
    }

    movies.append(movie_data)

# print(movies)

# select 간결하게 가져오기

# a_list = movie_code_soup.select(
#     'dl[class=lst_dsc] > dt > a')

# for a in a_list:
#     movie_title = a.text
#     movie_code = a['href'].split('code=')[1]
#     print(movie_code, ' ', movie_title)



# 영화 리뷰 & 평점 가져오기 (08.05)

# 영화 리뷰의 경우 headers 체크를 따로 하지 않아서 굳이 보낼 필요 없음
# headers = {
#     'authority': 'movie.naver.com',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-dest': 'iframe',
#     'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
#     'accept-language': 'ko-KR,ko;q=0.9,en;q=0.8,en-US;q=0.7',
#     'cookie': 'NNB=U4QXOA2MO2XV4; NID_AUT=SVTlnwKUOIVe/tUEtyzZoNs1TbOmgmMAn2YE9q9bvl1fCxZZeQ77Z5LXaI8FMRI5; NID_JKL=m8zC2bRTSH0KYSHwV3yebLj92mMjJeOEueFz3Wx19/c=; NRTK=ag#20s_gr#2_ma#-2_si#1_en#1_sp#1; NaverSuggestUse=use%26unuse; ASID=dd905ae700000171e868598c00000065; NDARK=Y; nx_ssl=2; MM_NEW=1; NFS=2; MM_NOW_COACH=1; NM_THUMB_PROMOTION_BLOCK=Y; _ga=GA1.1.675972496.1596511587; _ga_7VKFYR6RV1=GS1.1.1596524056.2.1.1596524159.60; notSupportBrowserAlert=true; page_uid=UyVIxlp0YiRssM+CxE4ssssstWK-031328; NID_SES=AAABjcBt5Df0FwFFpfBHiRZBQR4RI0LusensqJQu1kW3ceGlgno3DvcdgqPZht7J3USrCZ6p0TAhMuKOLSLf9KB57bx7iebSLImIiAZ1tRYdQozyHYwgO/5LeXVQQmu5FUuXn24b40YYr5cETaehdOyzp0XCfinuG4Z3S6DBM80PMKjpJnJi9v5+9bH57qabGCYJeGlC13SBfFMMJktAAwFSUAl/bX6XMIyE/3lqs+RPMWgOO2iXRLFjGIlUM41LTxAX8LizCJDPvIS6yPX6j6dyDNZXw4RvAj9VEK5SYXBE78YGTc2gZjn2rD3tOfHunbwM2UsAhPFZNwuBkTMA0SGElotksjtCfb1/gKO97FRbkWB86xmdoHMsDwRs9jiapJI5MR9yp1cIeU8VirCkk/z112RpBU8hNyoZTJVMXJVXVuQAUXGV2+oHBXK/A8mgCvzEk24BXSK16rAbFbnYFDrXdzWLKBXQV5ySNKcs7i39y5EdPlFRoXhQV7QFi7SSQKQX3P3tF5HWsLoVlOASzx2OaZU=; JSESSIONID=4E6D79ACC6032AD1DD061C4ACD8930D4; csrf_token=b639f4fc-d16f-4c46-9ed4-496d7676a55f',
# }

for movie in movies:
    movie_code = movie['code']
    # print(movie_code)

    # REVIEW_URL = f'https://movie.naver.com/movie/bi/mi/point.nhn?code={movie_code}#tab'
    # review_response = requests.get(REVIEW_URL)
    # print(review_response.text)
    # 위의 방법으로 body > div > div > div.score_result > ul > li 하면 아무 것도 안온다.
    # 왜냐하면, 경로로 가져와지는 body 부분은 iframe이라서, 이에 대한 방법으로 cURL을 사용한다.

    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    review_response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=params) # header=header 생략
# print(review_response.text)

    review_soup = BeautifulSoup(review_response.text, 'html.parser')

    review_list = review_soup.select(
        'body > div > div > div.score_result > ul > li'
    )

    for i, rv in enumerate(review_list):
        star_score = rv.select_one('div.star_score > em').text
        try:
            review = rv.select_one(f'div.score_reple > p > span#_filtered_ment_{i} > span > a')['data-src']
      
        except:
            review = rv.select_one(f'div.score_reple > p > span#_filtered_ment_{i}').text.strip()
       
        print(star_score)
        print(review, '\n')

    '''
    # 또 다른 방법 (조건문 사용) 
    count = 0

    for review in review_list:
        score = review.select_one('div.star_score > em').text
        reple = ''

        # 일반적인 경우 먼저 처리 (일반적인 것을 먼저 처리하는 것이 효율적이다)
        if review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}') is None:
            reple = review.select_one(
                f'div.score_reple > p > span#_filtered_ment_{count}').text.strip()
        # 리뷰가 긴 경우 처리
        elif review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}'):
            reple = review.select_one(
                f'div.score_reple > p > span#_filtered_ment_{count} > span > a')['data-src']

        print(score, reple)

        count += 1
    '''