import json
import kor_char_parser
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

def load_data_and_labels():
    """
    Loads polarity data from files, splits the data into words and generates labels.
    Returns split sentences and labels.
    """
    # Load data from files
    #positive_examples = list(open("./data/rt-polarity.pos", "r", encoding='latin-1').readlines())
    #positive_examples = [s.strip() for s in positive_examples]
    #negative_examples = list(open("./data/rt-polarity.neg", "r", encoding='latin-1').readlines())
    #negative_examples = [s.strip() for s in negative_examples]

    # split comments and scores
    dataset_path = "movie_score.json"
    with open(dataset_path, encoding='utf-8') as f:
        data = json.loads(f.read())

    comments = []
    scores = []
    for review in data:
        comments.append(review["comment_text"])
        scores.append(review["score"])

    # Split by words
    #x_text = positive_examples + negative_examples
    #x_text = [clean_str(sent) for sent in x_text]
    #x_text = [s.split(" ") for s in x_text]
    # Generate labels
    #positive_labels = [[0, 1] for _ in positive_examples]
    #negative_labels = [[1, 0] for _ in negative_examples]
    return [comments, scores]

def load_data():
    """
    Loads and preprocessed data for the dataset.
    Returns input vectors, labels, vocabulary, and inverse vocabulary.
    """
    # Load and preprocess data
    sentences, labels = load_data_and_labels()
    sentences_padded = pad_sentences(sentences)
    vocabulary, vocabulary_inv = build_vocab(sentences_padded)
    x, y = build_input_data(sentences_padded, labels, vocabulary)
    return [x, y, vocabulary, vocabulary_inv]


if __name__ == '__main__':
    comments, labels = load_data_and_labels()
    print(labels)