import json
import kor_char_parser
from pprint import pprint

# get data from json


# split comments and scores
class Dataset:
    def __init__(self, max_length: int):
        dataset_path = "movie_score.json"
        with open(dataset_path, encoding='utf-8') as f:
            self.data = json.loads(f.read())

        self.comments = []
        self.scores = []
        for review in data:
            comments.append(review["comment_text"])
            scores.append(review["score"])

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.comments[idx], self.scores[idx]

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

