# -*- coding: utf-8 -*-
"""NaverMovie.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17ETcTCkpE5O5b-oqtqRh0BpQmnDpi8gY
"""

import pandas as pd
import numpy as np
from konlpy.tag import Okt
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_naver_mv_recommendation.settings')
import django
django.setup()





def naver_movie_data():
    print("데이터 불러오는 중...")
    data = pd.read_csv('./recommendapp/csv/navermovies2.csv')
    print("불러오기 완료.")

    # 0번째 열은 순위와 같은 값을 갖는 중복된 열이므로 제외
    data = data.iloc[:, 1:] 

    # 나라와 상영시간을 분리하여 각각의 열 생성
    data[['나라', '상영시간']] = data['나라,상영시간'].str.split(', ', expand=True) 
    # 나라와 상영시간이 같이 있던 열은 삭제
    del data['나라,상영시간'] 

    genre_count = data['장르'].value_counts()
    genres = genre_count.index[:10].tolist() # 장르 목록 리스트화
    # 장르가 genres에 포함되지 않는 행 삭제
    data = data[data['장르'].isin(genres)]

    # 줄거리가 '줄거리 준비중입니다. / 줄거리 정보가 없습니다. / 줄거리 정보가 없습니다'인 행 삭제
    no_summary = ['줄거리 준비중입니다.', '줄거리 정보가 없습니다.', '줄거리 정보가 없습니다']
    data = data[~data['줄거리'].isin(no_summary)]

    # '평점'이 4 이하인 행 삭제
    data = data[data['평점'] > 4]
    data.shape

    # '주연'과 '줄거리'가 null 값인 행 삭제
    data = data.dropna(subset=['주연', '줄거리'])

    # '감독'과 '주연'의 값을 공백을 기준으로 나누는 하나의 문자열화
    # 이름이 두 어절 이상인 사람들을 하나로 인지가히기 위해 먼저 공백을 없앤 후, 쉼표를 공백으로 replace 한다.
    print("토큰화 진행 중...")
    data['감독'] = data['감독'].str.replace(' ', '').str.replace(',', ' ')
    data['주연'] = data['주연'].str.replace(' ', '').str.replace(',', ' ')

    # '줄거리'에 위에서 정의한 split_data 함수를 적용해 'keywords'를 만든 후, 위에서와 같이 하나의 문자열화
    data['keywords'] = data['줄거리'].apply(split_data)
    data['keywords'] = data['keywords'].apply(lambda x : ' '.join(x))

    # 순위(인덱스) 순으로 정렬 후, 0부터 시작하는 순위에 1씩 더한다.
    data = data.sort_index()
    data['순위'] += 1

    # 제목이 같은 중복 데이터 삭제
    data = data.drop_duplicates(subset='제목')
    
    # 인덱스 재설정
    data = data.reset_index(drop=True)
    print("토큰화 완료 및 'data' 값 반환")
    return data



def split_data(x):
    nlp = Okt()
    try:
        nouns = nlp.nouns(x)
        nouns = [n for n in nouns if len(n) > 1]
        return nouns

    except:
        return 'None'

def input_mv_name():
    mv_name = input("좋아하는 영화 이름을 입력하세요. ")
    return mv_name

def movie_pred(data, mv_name):
    # '장르', '감독', '주연', 'keywords'를 하나의 문자열화
    print("'data'값 불러오는 중...")
    mv = data['장르'] + ' ' +  data['감독'] + ' ' + data['주연'] + ' ' + data['keywords']
    print("불러오기 완료.")

    vec = CountVectorizer(ngram_range=(1, 2))
    matrix = vec.fit_transform(mv)

    similarity = cosine_similarity(matrix, matrix)
    count_similar_index = np.argsort(-similarity)
    
    # print("좋아하는 영화 이름을 입력하세요.")
    input_movie = mv_name
    print("영화 추천 중...")
    
    movie_index = data[data['제목'] == input_movie].index.values
    similar_movies = count_similar_index[movie_index, 0:10]

    similar_movies_index = similar_movies.reshape(-1)
    result = data.iloc[similar_movies_index, 1:4]

    result.to_csv("result.csv")
    # print(type(result))

    return result

def df_to_list(result):
    result = pd.read_csv('result.csv')
    
    # result의 각 레이블들을 3개의 시리즈로 분리
    mv_name = result['제목']
    mv_poster = result['포스터']
    mv_rating = result['평점']

    # 영화 정보가 담긴 딕셔너리 값들을 담기 위한 리스트
    list_movie = []
    
    # 영화 정보들을 담고 이를 딕셔너리화 하기 위한 리스트
    # 이런 번거로운 일을 하는 이유는, 딕셔너리로 반복문을 통해 list_movie에 append 하면,
    # 기존의 list_movie에 append 된 딕셔너리 값들까지 바뀌어 버리는 문제가 발생하기 때문
    list_ele = []

    # list_movie에 영화 정보들을 append 
    for i in range(10):
        list_ele = [['name', mv_name[i]], ['poster', mv_poster[i]], ['rating', mv_rating[i]]]
        list_ele = dict(list_ele)
        list_movie.append(list_ele)

    return list_movie