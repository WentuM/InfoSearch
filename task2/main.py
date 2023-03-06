from os import listdir
from os.path import isfile, join
import re
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation, digits
from collections import Counter
from autocorrect import Speller
import language_tool_python

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

nltk.download("stopwords")

words_path = 'tokens.txt'
tokens_path = 'tokens_lemma.txt'
loads_path = '../task1/loads'

loads = [f for f in listdir(loads_path) if isfile(join(loads_path, f))]
mystem = Mystem()
russian_stopwords = stopwords.words("russian")
words = []

def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return not alphabet.isdisjoint(text.lower())

if __name__ == '__main__':
    files_len = len(loads)
    tool = language_tool_python.LanguageTool('ru-RU')
    for i in range(files_len):
        file = loads[i]
        html_file = open(loads_path + '/' + file, "r", encoding="utf-8")
        html = html_file.read().replace("<br>", " ")
        html_file.close()
        parsed_html = BeautifulSoup(html, features="html.parser")
        sentence = re.sub(r"[\n\s.,:–\\?—\-!()/»><;'*+©\"]+", " ", parsed_html.text, flags=re.UNICODE).lower()
        tokens = [token for token in sentence.split(" ") if token not in russian_stopwords \
                  and token != " " \
                  # and len(tool.check(token)) == 0 \
                  and token.strip() not in punctuation \
                  and (re.search('\d+', token) is None) \
                  and (re.search('«', token) is None) \
                  and len(token) > 1] \
                  # and print(tool.check(token))]
        print('ненормально: ')
        print(tokens)
        tokens = [token for token in tokens if match(token)]
        print('ненормально русские: ')
        print(tokens)
        tokens = [token for token in tokens if len(tool.check(token)) == 0]
        print('нормально: ')
        print(tokens)
        words.extend(tokens)

    words_file = open(words_path, "a", encoding="utf-8")
    words_dict = Counter(words)

    for key, value in words_dict.items():
        words_file.write(key + "\n")
    words_file.close()

    tokens = {}

    words_len = len(words)
    for i in range(words_len):
        word = words[i]
        token = mystem.lemmatize(word)[0]
        if token in tokens:
            tokens.get(token).add(word)
        else:
            tokens[token] = set(word)

    tokens_file = open(tokens_path, "a", encoding="utf-8")
    for key, words_tokens in tokens.items():
        tokens_file.write(key + " ")
        for word in words_tokens:
            if word != key and len(word) > 1:
                tokens_file.write(word + " ")
        tokens_file.write("\n")
