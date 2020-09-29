from django.shortcuts import render
from django.http import HttpResponse
from NaverMovie import naver_movie_data, movie_pred, df_to_list
import pandas as pd

# Create your views here.

def home(request):
    return render(request, 'home.html')

def result(request):
    # home에서 받은 검색 결과를 mv_name에 저장
    mv_name = request.POST['mv_name']
    
    # NaverMovie.py에서 함수를 불러온 뒤에 그 함수에 name을 넣어서 반환한 값을 data에 저장
    data = naver_movie_data()

    data_df = movie_pred(data, mv_name)
    mv_info = df_to_list(data_df)

    return render(request, 'result.html', {'mv_info' : mv_info})

