import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def data_to_list(data):
    result = []

    for d in data:
        for key in d:
            temp = []
            for w in d[key]:
                temp.append(w[0])
            result.append(temp)

    for i in range(len(result)):
        temp = ''
        for j in result[i]:
            temp += j.replace(' ', '') + ' '
        result[i] = temp[:-1]

    return result


def similiar_check(data, user):
    m_list = data_to_list(data)
    m_list.append(user)
    
    vec = CountVectorizer(ngram_range=(1, 2))
    matrix = vec.fit_transform(m_list)

    similarity = cosine_similarity(matrix, matrix)

    count_similar_index = np.argsort(-similarity)

    similar = count_similar_index[-1, 1:4]

    similar_index = similar.reshape(-1)

    result = []
    for i in similar_index:
        result += list(data[i].keys())
    
    return result[0], result[1], result[2]