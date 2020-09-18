from gensim.models import FastText
# from gensim.test.utils import common_texts # 테스트로 학습할 데이터를 불러오기
from gensim.test.utils import datapath
from gensim.utils import tokenize
from gensim import utils
from gensim.test.utils import get_tmpfile
import numpy as np
from gensim.models.fasttext import load_facebook_vectors


# # # 테스트로 학습할 소량의 데이터 출력
# # print(common_texts)
#
# # 데이터 불러오기
# absolute_path = 'C:/Users/jang lee uk/PycharmProjects/ai_school_project/voice_recognition_ordering_system/jang262_branch/GJAI_WarmingUpProject/AIJOA_Project//wiki.ko'
# file_name = 'wiki.ko.bin'
# # file_name = 'cc.ko.300.bin' # wiki.ko.bin
# corpus_file = datapath(absolute_path +'/'+ file_name)  # 데이터의 절대경로 상대경로는 안되나? 응 안돼
#
# # 다른 형식의 말뭉치가있는 경우 iterator 로 래핑하여 사용할 수 있다.
# # 반복자는 매번 문자열 목록을 생성해야하며 각 문자열은 별도의 단어 여야함. 나머지는 Gensim이 처리함.
# class MyIter(object):
#     def __iter__(self):
#         path = datapath('crime-and-punishment.txt') # 학습시킬 데이터의 절대경로
#         with utils.open(path, 'r', encoding='utf-8') as fin:
#             for line in fin:
#                 yield list(tokenize(line)) # yield는 generator사용시 return대신 사용되며 호출할때마다 한번씩 yield 값을 리턴함??
#
# # 모델 구축
# # vector_size (int) – 벡터의 차원 수
# # min_n (int) – ngram의 최소 문자 수
# # max_n (int) – ngram의 최대 문자 수
# # bucket (int) – 버킷 수
# # compatible_hash ( boolean ) – True 인 경우 Gensim 이전 버전과 호환되는 해시
# #                               함수 대신 Facebook 호환 해시 함수를 사용합니다.
#
# # model 객체화 # 우측 링크의 매개변수 참조 : https://radimrehurek.com/gensim/models/fasttext.html
# print("모델 객체 생성")
# model = FastText(size=1000, window=3, min_count=1, workers=4, sg=1)
# print("corpus_total_words 및 corpus_count 속성 설정")
# model.build_vocab(sentences=corpus_file) # build_vocab()메소드는 corpus_total_words (및 corpus_count) 모델 속성을 설정
#
# # 말뭉치의 단어 수 : 모델은 학습률 (알파)을 올바르게 관리하고 정확한 진행률 추정치를 제공하기 위해 total_words 매개 변수가 필요
# # corpus_count와 corpus_total_words의 차이는 아직 모르겠음 ****
# total_examples = model.corpus_count
# total_words = model.corpus_total_words
# print(total_words)
# print(total_examples)
#
# # model train
# print("model training start")
# model.train(corpus_file=corpus_file, total_words=total_words, epochs=500)
# # 다른 형식의 말뭉치가있는 경우 train 방법
# # model.train(sentences=MyIter(), total_examples=total_examples, epochs=5)
# print("model training end")
#
# # 모델 저장 : 저장경로는 절대 절대 절대 경로로 설정 안그러면 어만데 저장됨.
# save_name = "fasttext_test_model.model"
# fname = get_tmpfile(absolute_path +'/'+ save_name)
# print("model save start")
# model.save(fname)
# print("model save end")

# 저장했던 모델 불러오기 : 절대 경로임.
absolute_path = 'C:/Users/jang lee uk/PycharmProjects/ai_school_project/voice_recognition_ordering_system/jang262_branch/GJAI_WarmingUpProject/AIJOA_Project//wiki.ko'
save_name = "fasttext_test_model.model"
fname = get_tmpfile(absolute_path +'/'+ save_name)
print("model load start")
model = FastText.load(fname)
print("model load end")

# # 불러온 모델에 이어서 학습하기
# # 모델이 있으면 model.wv 속성을 통해 키가 지정된 벡터에 액세스 할 수 있다.
# # print('computation' in model.wv.vocab)  # New word, currently out of vocab
# old_vector = np.copy(model.wv['computation'])  # Grab the existing vector
# # 추가로 학습할 데이터
# new_sentences = [
#     ['computer', 'aided', 'design'],
#     ['computer', 'science'],
#     ['computational', 'complexity'],
#     ['military', 'supercomputer'],
#     ['central', 'processing', 'unit'],
#     ['onboard', 'car', 'computer'],
# ]
# # corpus_total_words (및 corpus_count) 모델 속성을 추가 설정
# # 이어서 학습시킬때에는 update=True로 설정해야 기존 학습한 어휘가 추가된체로 학습함.
# model.build_vocab(new_sentences, update=True)  # Update the vocabulary
# # 추가 학습
# model.train(new_sentences, total_examples=len(new_sentences), epochs=model.epochs)
# new_vector = model.wv['computation']
# # print(np.allclose(old_vector, new_vector, atol=1e-4))  # Vector has changed, model has learnt something
# # print('computation' in model.wv.vocab)  # Word is still out of vocab

print("폴더버거핫치킨 유사도 확인")
for w, sim in model.wv.similar_by_word('폴더버거핫치킨', 10):
    print(f'{w}: {sim}')

print(f"'폴더버거핫치킨'과 '폴더버그핫치킨'의 유사도: {model.wv.similarity('폴더버거핫치킨', '폴더버그핫치킨')}")
print(f"'아이언맨'과 '헐크'의 유사도: {model.wv.similarity('아이언맨', '헐크')}")
print(f"'아이언맨'과 '스파이더맨'의 유사도: {model.wv.similarity('아이언맨', '스파이더맨')}")




# # # 학습된 데이터의 차원 줄이는 방법 : 먼가 못하고 있음...
# # file_name = 'cc.ko.300.bin' # wiki.ko.bin
# # corpus_file = datapath(absolute_path +'/'+ file_name)
# # print(corpus_file.get_dimension())
# # utils.reduce_model(corpus_file, 100)
# # print(corpus_file.get_dimension())


# # facebook에서 미리 학습 시켜놓은
# # gensim.models.fasttext.load_facebook_vectors() 함수 사용 시
# file_name = 'wiki.ko.bin' # cc.ko.300.bin
# cap_path = datapath(absolute_path +'/'+ file_name)
# wv = load_facebook_vectors(cap_path)
# print('landlord' in wv.vocab)  # Word is out of vocabulary
# oov_vector = wv['landlord']
# print('landlady' in wv.vocab)  # Word is in the vocabulary
# iv_vector = wv['landlady']
#
# # 어휘 및 어휘 외 단어에 대한 단어 벡터 검색 :
# existent_word = "computer"
# print(existent_word in model.wv.vocab)
# computer_vec = model.wv[existent_word]  # numpy vector of a word
# oov_word = "graph-out-of-vocab"
# print(oov_word in model.wv.vocab)
# oov_vec = model.wv[oov_word]  # numpy vector for OOV word

# # 모델로 다양한 NLP 단어 작업을 수행 할 수 있으며 그중 일부는 이미 내장되어 있습니다.
# similarities = model.wv.most_similar(positive=['computer', 'human'], negative=['interface'])
# most_similar = similarities[0]
# similarities = model.wv.most_similar_cosmul(positive=['computer', 'human'], negative=['interface'])
# most_similar = similarities[0]
# not_matching = model.wv.doesnt_match("human computer interface tree".split())
# sim_score = model.wv.similarity('computer', 'human')
# # 단어 유사성에 대한 인간의 의견과의 상관 관계 :
# similarities = model.wv.evaluate_word_pairs(datapath('wordsim353.tsv'))
# # 그리고 단어 비유 :
# analogies_result = model.wv.evaluate_word_analogies(datapath('questions-words.txt'))