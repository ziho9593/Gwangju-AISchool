from gensim import models
from gensim.models import FastText
from gensim.test.utils import common_texts # 테스트로 학습할 데이터를 불러오기
from gensim.test.utils import datapath
from gensim.utils import tokenize
from gensim import utils
from gensim.test.utils import get_tmpfile
import os
import numpy as np
from django.conf import settings

absolute_path = 'C:/Users/HAN/Desktop/WarmingUpProject/AIJOA_Project/wiki.ko'

def main():
    class MyIter(object):
        def __iter__(self):
            # absolute_path = r'C:\Users\NA\Desktop\Workspace\GJAI_WarmingUpProject\AIJOA_Project\wiki.ko'
            file_name = 'voice.txt'
            path = datapath(absolute_path +'/'+ file_name) # 학습시킬 데이터의 절대경로
            with utils.open(path, 'r', encoding='UTF-8') as fin:
                for line in fin:
                    yield list(tokenize(line))


    # 데이터 불러오기
    # absolute_path = r'C:\Users\NA\Desktop\Workspace\GJAI_WarmingUpProject\AIJOA_Project\wiki.ko'
    file_name = 'wiki.ko.bin'
    # file_name = 'cc.ko.300.bin' # wiki.ko.bin
    corpus_file = datapath(absolute_path +'/'+ file_name)  # 데이터의 절대경로 상대경로는 안되나? 응 안돼


    # 모델 구축
    # model 객체화 # 우측 링크의 매개변수 참조 : https://radimrehurek.com/gensim/models/fasttext.html
    print("모델 객체 생성")
    # model = FastText(size=1000, window=3, min_count=3, workers=4, sg=1)
    model = models.fasttext.load_facebook_model(corpus_file)


    # 불러온 모델에 이어서 학습하기
    # MyIter()로 불러온 데이터 new_sentences 리스트에 담기
    new_sentences = []
    for i in MyIter():
        new_sentences.append(i)
    print(new_sentences)

    # MyIter()로 불러온 데이터양 늘리기
    new_sentences = new_sentences * 10000
    print(len(new_sentences))


    # corpus_total_words (및 corpus_count) 모델 속성을 추가 설정
    # 이어서 학습시킬때에는 update=True로 설정해야 기존 학습한 어휘가 추가된체로 학습함.
    print("추가 어휘구성")
    model.build_vocab(new_sentences, update=True)  # Update the vocabulary
    print("추가 어휘구성 끝")
    # 추가 학습
    print("추가 학습")
    model.train(new_sentences, total_examples=len(new_sentences), epochs=model.epochs)
    print("추가 학습 끝")


    # 모델 저장 : 저장경로는 절대 절대 절대 경로로 설정 안그러면 어만데 저장됨.
    save_name = "wiki_ko_v3.model"
    fname = get_tmpfile(absolute_path +'/'+ save_name)
    print("model save start")
    model.save(fname)
    print("model save end")


    # 저장했던 모델 불러오기 : 절대 경로임.
    # absolute_path = r'C:\Users\NA\Desktop\Workspace\GJAI_WarmingUpProject\AIJOA_Project\wiki.ko'
    file_name = "wiki_ko_v3.model"
    fname = get_tmpfile(absolute_path +'/'+ file_name)
    print("model load start")
    model = FastText.load(fname)
    print("model load end")

    menu_list = {
        '폴더버거 핫치킨':['골드버거 치킨','오늘도 봐봐 치킨','오늘도 보고 와 치킨','불도 먹었어 치킨',
                    '골드버거 핫치킨', '골드버거 치킨', '월드 보고 아침에', '오늘도 보고 와 치킨',
                    '폴더 버거 킹', '홀더 버거 치킨', '뭘 더 먹어 치킨', '너 먹어 치킨', '뭐 먹어 치킨'],
        '폴더버거 비프':['골드버그 비프', '올더 버거 비프', '폴더 버거 비프', '골드버그 비프 세트',
                '올더 버거 비프 세트', '어디서 먹어 핑크색', '물 더 먹어 비트 세트', '골드버그 비프 세트',
                '올 더 버거 비틀 세트', '홀더 버거 비프', '뭘 더 먹어 비프', '너 먹어 피프 세트',
                '뭐 먹어 비프'],
        '리아미라클버거':['리아미라클버거', '미아 미라클버거', '리아미라클버거 세트', '미라클버거 세트','리아 미라클 버거 세트'],
        '와규 에디션 투':['외규에디션 2', '마귀 에디션 2', '와규에디션 2', '와 귀신 전화', '월요일 좀 주세요 전화',
                    '와규에디션 2 세트', '와규에디션 2 세트', '목요일 샘플 세트'],
        '더블엑스투':['브렉시트', '더블엑스 2', '더블 X2 세트', '저번에 지출 세트', '버그 렉스필드 전화',
                '노래 치킨 세트', '더블 X2 세트', '더블엑스 풀세트', '더블엑스 두 세트'],
        '티렉스':['티렉스 버거', '티렉스 버거 세트', '티렉스버거세트', '티렉스버거 찾아',
            '티렉스 버거 세트 두 개', '티렉스버거세트 두 개'],
        '클래식 치즈버거':['클래식 치즈버거', '클래식 치즈버거 세트 하나', '클래식 치즈버거 틀어',
                    '클래식 치즈버거 세트', '클래식 치즈버거 세트 두 개'],
        '한우불고기':['한우 불고기', '한우불고기 세트 하나', '한우 불고기 집 전화', '한우 불고기 제주 TV',
                '한우불고기 두 개', '한우불고기 세트 두 개'],
        '모짜렐라 인 더 버거 베이컨':['모짜렐라인 더 버거', '모짜렐라인 더 버거 세트 하나',
                        '모짜렐라 인더버거 베트남', '모짜렐라인 더 버거 세트 두 개',
                        '모짜렐라인 더 버거 세트'],
        # '모짜렐라 in the 버거':['모짜렐라인 더 버거', '모짜렐라인 더 버거 세트 하나',
        #                    '모짜렐라 인더버거 베트남', '모짜렐라인 더 버거 세트 두 개',
        #                    '모짜렐라인 더 버거 세트'],
        # '모짜렐라 인 더 버거':['모짜렐라인 더 버거', '모짜렐라인 더 버거 세트 하나',
        #                    '모짜렐라 인더버거 베트남', '모짜렐라인 더 버거 세트 두 개',
        #                    '모짜렐라인 더 버거 세트'],
        '에이지버거':['az버거', 'az버거 세트', '에이지버거', '에이지버거 세트', '아재버거', '아재버거 세트 하나', '거제도 가서 찾아',
                '아재 동생 두 개', '아재버거세트 두 개', '아재버거 세트 두 개'],
        'az버거':['az버거', 'az버거 세트', '에이지버거', '에이지버거 세트', '아재버거', '아재버거 세트 하나', '거제도 가서 찾아',
                '아재 동생 두 개', '아재버거세트 두 개', '아재버거 세트 두 개'],
        '에이제트버거':['az버거', 'az버거 세트', '에이제트버거', '에이제트버거 세트', '아재버거', '아재버거 세트 하나', '거제도 가서 찾아',
                '아재 동생 두 개', '아재버거세트 두 개', '아재버거 세트 두 개'],
        '원조 빅불':['원조빅불', '원조빅불 세트', '원조빅불세트', '언제 도착하나', '물제 를 풀 세트',
                '원조 빅불 세트', '오늘 이불세트'],
        '핫크리스피버거':['핫크리스피버거', '하트스피가방', '핫크리스피버거 세트', '크리스피 버거 세트',
                '핫 크리스피버거 세트', '하트 스트커 세트'],
        '불고기버거':['불고기 버거', '불고기 버거 세트 하나', '불고기 버거 세트', '불고기버거 세트 두 개'],
        '데리버거':['데리버거', '데리버거 세트 하나', '데리버거 찾아', '데리버거 두 개', '데리버거 세트 두 개',
                '데리버거세트 두 개'],
        '치킨버거':['치킨버거', '치킨 먹어', '치킨 버거 세트', '치킨 먹었다', '치킨 먹어서 두 개',
                '치킨 버거 세트 두 개'],
        '새우버거':['새우버거', '재봉 설탕', '새우버거 세트', '일본어 태어나', '여보 가서 켜',
                '새우버거 속']
    }


    # 메뉴오탈과 메들 사이의 유사도
    print("메뉴오탈과 메들 사이의 유사도 비교 파일 생성 시작")
    for key1 in menu_list.keys():
        file_name = f'{key1}메뉴의 오탈자와 전체메뉴들과의 유사도.txt'
        for value in menu_list[key1]:
            for key2 in menu_list.keys():
                # print(f"메뉴'{key1}'의 오탈자 '{value}'와 메뉴명'{key2}'와의 유사도: {model.wv.similarity(value, key2)}")
                if file_name not in os.listdir(absolute_path):
                    with open(absolute_path+'/'+file_name, 'w', encoding='utf-8') as file_data:
                        file_data.write(f"'{key1}'의 오탈자 '{value}'와 메뉴명'{key2}'와의 유사도: {model.wv.similarity(value, key2)}\n")
                else:
                    with open(absolute_path+'/'+file_name, 'a', encoding='utf-8') as file_data:
                        file_data.write(f"'{key1}'의 오탈자 '{value}'와 메뉴명'{key2}'와의 유사도: {model.wv.similarity(value, key2)}\n")
    print("메뉴오탈과 메들 사이의 유사도 비교 파일 생성 종료")

def getwordsim(target, menulist):

    print("메뉴오탈자 단어와 메뉴들 사이의 유사도 비교 파일 생성 시작")
    simlist={}
    menulist = getattr(settings, 'MENULIST')
    model = getattr(settings, 'MODEL')
    for key in menulist.keys():
        simlist[key] = model.wv.similarity(target,key)
        print(f"음성인식으로 입력된 값 '{target}'과 메뉴명'{key}'와 와의 유사도: {simlist[key]}")

    mostsimword = max(simlist, key=simlist.get)
    print(f"유사도 측정 결과 '{mostsimword}'선정")
    
    if max(simlist.values()) < 0.7: # 0.8로 올려도 될 듯?
        return -1
    else:
        return mostsimword
        
def order_dict_init():
    menulist = getattr(settings, 'MENULIST')
    return {key : 0 for key in menulist.keys()}

if __name__ == "__main__":
    main()





