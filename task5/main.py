from math import sqrt
from typing import List

import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

tokens = list(set(open('task2/tokens.txt').read().splitlines()))
lemmas = list(word.split(' ')[0] for word in open('task2/tokens_lemma.txt').read().splitlines())

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stopwords = stopwords.words("russian")


def similarity(df1, df2):
    merged_df = pd.merge(df1, df2, on='word')
    x, y = np.array(merged_df['td-idf_x']), np.array(merged_df['td-idf_y'])
    x_r, y_r = x - np.mean(x), y - np.mean(y)
    d = np.sqrt(np.sum(x_r ** 2) * np.sum(y_r ** 2))
    if d:
        result = np.sum(x_r * y_r) / d
        return sqrt(result ** 2)
    return .0


def clean_tokens(text: str):
    return set([w for w in nltk.word_tokenize(text) if w not in stopwords and len(w) > 1])


def get_tokens_data_frame(inp):
    tokens_vectorizer = TfidfVectorizer(analyzer=clean_tokens, vocabulary=tokens)
    token_fit_transform = tokens_vectorizer.fit_transform(inp)

    tokens_idf = pd.DataFrame(tokens_vectorizer.idf_, index=tokens, columns=["idf"])
    tokens_tfidf = pd.DataFrame(token_fit_transform.T.todense(), index=tokens, columns=["tf-idf"])
    tokens_result_df = pd.concat([tokens_idf, tokens_tfidf], axis=1)

    return tokens_result_df.rename(columns={tokens_result_df.columns[0]: 'word'})


def get_tokens_dt_as_pd(tokens_dt):
    with open(f"tokens.txt", "w") as tokens_file:
        tokens_file.write(tokens_dt.to_csv(sep=" ", header=False))

    return pd.read_csv(
        'tokens.txt',
        delimiter=' ',
        names=['word', 'idf', 'td-idf']
    )


def process(input_strings: List[str]):
    tokens_df = get_tokens_data_frame(input_strings)
    tokens_pd = get_tokens_dt_as_pd(tokens_df)

    result = dict()
    for i in range(110):
        tokens_for_text_read = pd.read_csv(
            f'task4/lemmas/выкачка-{i + 1} (tf-idf).txt',
            delimiter=' ',
            usecols=range(1, 4),
            names=['word', 'idf', 'td-idf']
        )
        result[i + 1] = similarity(tokens_for_text_read, tokens_pd)

    return sorted(result.items(), key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    while True:
        print("Введите запрос: ", end="")
        input_str = input().split(" ")

        for k, v in process(input_str):
            print(str(k) + " " + str(v))
