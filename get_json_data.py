import json
import numpy as np
import re
from kor_char_parser import decompose_str_as_one_hot
from pprint import pprint


def preprocess(data: list, max_length: int):
    """
     입력을 받아서 딥러닝 모델이 학습 가능한 포맷으로 변경하는 함수입니다.
     기본 제공 알고리즘은 char2vec이며, 기본 모델이 MLP이기 때문에, 입력 값의 크기를 모두 고정한 벡터를 리턴합니다.
     문자열의 길이가 고정값보다 길면 긴 부분을 제거하고, 짧으면 0으로 채웁니다.
    :param data: 문자열 리스트 ([문자열1, 문자열2, ...])
    :param max_length: 문자열의 최대 길이
    :return: 벡터 리스트 ([[0, 1, 5, 6], [5, 4, 10, 200], ...]) max_length가 4일 때
    """
    vectorized_data = [decompose_str_as_one_hot(datum, warning=False) for datum in data]
    zero_padding = np.zeros((len(data), max_length), dtype=np.int32)
    for idx, seq in enumerate(vectorized_data):
        length = len(seq)
        if length >= max_length:
            length = max_length
            zero_padding[idx, :length] = np.array(seq)[:length]
        else:
            zero_padding[idx, :length] = np.array(seq)
    return zero_padding

def mask_data(comments, title, people):
    comments = re.sub(title, '', comments)
    for person in people:
        comments = re.sub(person, '', comments)
    return comments

def load_data_and_labels(data_name):
    """
    Loads polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # load data
    with open(data_name, encoding='utf-8') as f:
        data = json.loads(f.read())

    # split comments and scores

    comments = []
    scores = []
    for review in data:
        if int(review["score"]) == 10:
            pass
        else:
            comments.append(mask_data(review["comment_text"], review["title"], review["people"]))
            scores.append(int(review["score"]) - 1)
    print(set(scores))
    
    return [comments, scores]

def load_data(data_name):
    """
    Loads and preprocessed data for the dataset.
    Returns input vectors, labels, vocabulary, and inverse vocabulary.
    """
    # Load and preprocess data
    sentences, labels = load_data_and_labels(data_name)
    max_len = 200
    sentences_padded = preprocess(sentences, max_len)
    return [sentences_padded, labels]


if __name__ == '__main__':
    data_name = "movie_score.json"
    embedded_sentences, labels = load_data(data_name)

