import pandas as pd

result = pd.read_csv('test.csv')

mv_name = result['제목']
mv_poster = result['포스터']
mv_rating = result['평점']

list_movie = []
list_ele = []

for i in range(9):
    list_ele = [['name', mv_name[i]], ['poster', mv_poster[i]], ['rating', mv_rating[i]]]
    list_ele = dict(list_ele)
    list_movie.append(list_ele)

# for i in list_movie:
#     print(i)

print(list_movie)