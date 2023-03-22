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
import numpy as np

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

countDocumentsWithNeedWord = {}

def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return not alphabet.isdisjoint(text.lower())

def makeDicWithWordInCountFiles():
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
        tokens = [token for token in tokens if match(token)]

        tokens = [token for token in tokens if len(tool.check(token)) == 0]

        words_unic = set(tokens)

        for word in words_unic:
            if word in countDocumentsWithNeedWord:
                countDocumentsWithNeedWord[word] += 1
            else:
                countDocumentsWithNeedWord[word] = 1

        print(f"file-make {i}")

if __name__ == '__main__':
    files_len = len(loads)
    tool = language_tool_python.LanguageTool('ru-RU')

    makeDicWithWordInCountFiles()
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

        tokens = [token for token in tokens if match(token)]
        tokens = [token for token in tokens if len(tool.check(token)) == 0]

        words = []
        words.extend(tokens)

        words_unic = set(tokens)

        fileWordDictionaries = {}

        fileWordDictionaries.update(dict.fromkeys(tokens, 0))
        for word in tokens:
            fileWordDictionaries[word] += 1


        currentFilesLength = i + 1

        file_path = f'../task4/tokens/выкачка-{currentFilesLength} (tf-idf)' + ".txt"
        tokens_file = open(file_path, "a", encoding="utf-8")
        for word in words_unic:
            tf = fileWordDictionaries[word] / len(tokens)
            idf = np.log10(files_len / countDocumentsWithNeedWord[word])
            tokens_file.write(f"{word} {idf} {tf * idf} \n")

        tokens = {}

        words_len = len(words)
        for i in range(words_len):
            word = words[i]
            token = mystem.lemmatize(word)[0]
            if token in tokens:
                tokens.get(token).add(word)
            else:
                tokens[token] = set([word])

        file_path = f'../task4/lemmas/выкачка-{currentFilesLength} (tf-idf)' + ".txt"
        tokens_file = open(file_path, "a", encoding="utf-8")

        for key, words_tokens in tokens.items():

            countLemmaWordsInfile = 0
            countLemmaWordsInAllFiles = 0

            for word in words_tokens:
                if len(word) > 1:
                    countLemmaWordsInfile += fileWordDictionaries[word]
                    countLemmaWordsInAllFiles += countDocumentsWithNeedWord[word]

            tf = countLemmaWordsInfile / len(tokens)
            idf = np.log10(files_len / countLemmaWordsInAllFiles)
            tokens_file.write(f"{key} {idf} {tf * idf} \n")

        print(f"file-result {i}")

