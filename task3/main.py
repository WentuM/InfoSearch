from os import listdir
from os.path import isfile, join
import re
import time

import nltk
import pymorphy2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation

nltk.download("stopwords")
nltk.download('punkt')
start_time = time.time()
russian_stopwords = stopwords.words("russian")
morph = pymorphy2.MorphAnalyzer()

# 1. Создать инвертированный список терминов (индекс)

def process_files(filenames):
    file_to_terms = {}
    for file in filenames:
        pattern = re.compile('[\W_]+')
        file_to_terms[file] = open(files_path + '/' + file, 'r', encoding='utf-8').read().lower()
        file_to_terms[file] = pattern.sub(' ', file_to_terms[file])
        file_to_terms[file] = word_tokenize(file_to_terms[file], language="russian")
        file_to_terms[file] = [w for w in file_to_terms[file] if w not in russian_stopwords
                               and w != " " \
                               and w.strip() not in punctuation \
                               and (re.search('\d+', w) is None) \
                               and (re.search('«', w) is None) \
                               and len(w) > 1]
        file_to_terms[file] = [morph.parse(w)[0].normal_form for w in file_to_terms[file]]
    return file_to_terms

def index_one_file(termlist):
    fileIndex = {}

    for index, word in enumerate(termlist):
        if word in fileIndex.keys():
            fileIndex[word].append(index)
        else:
            fileIndex[word] = [index]

    return fileIndex

def make_indices(termlists):
    total = {}
    for filename in termlists.keys():
        total[filename] = index_one_file(termlists[filename])
    return total

def fullIndex(regdex):
    total_index = {}
    for filename in regdex.keys():
        for word in regdex[filename].keys():
            if word in total_index.keys():
                if filename in total_index[word].keys():
                    total_index[word][filename].extend(regdex[filename][word][:])
                else:
                    total_index[word][filename] = regdex[filename][word]
            else:
                total_index[word] = {filename: regdex[filename][word]}
    return total_index


files_path = '../task1/loads'
files = [f for f in listdir(files_path) if isfile(join(files_path, f))]
files_len = len(files)
file_names = []

# 2. Реализовать булев поиск по построенному индексу

def one_word_query(word):
    pattern = re.compile('[\W_]+')
    word = pattern.sub(' ', word)

    if word in total_index.keys():
        return [filename for filename in total_index[word].keys()]
    else:
        return []


# 'OR'
def free_text_query(string):
    result = []
    for word in prepare_query(string):
        result += one_word_query(word)
    return list(set(result))


# 'AND'
def strict_text_query(string):
    result = []
    for word in prepare_query(string):
        result = list(set(result) & set(one_word_query(word))) if result \
            else set(one_word_query(word))
    return result

# 'NOT'
def not_phrase_query(string):
    prepared_query = prepare_query(string)
    listOfLists, result = [], []

    for word in prepared_query:
        listOfLists.append(one_word_query(word))
    setted = set(listOfLists[0]).intersection(*listOfLists)

    for filename in setted:
        temp = []
        for word in prepared_query:
            temp.append(total_index[word][filename][:])
        for i in range(len(temp)):
            for ind in range(len(temp[i])):
                temp[i][ind] -= i
        if set(temp[0]).intersection(*temp):
            result.append(filename)

    result = [filename for filename in regular_index.keys() if filename not in result]
    return [result, string]


def prepare_query(string):
    string_words = word_tokenize(string, language="russian")
    string_words = [w for w in string_words if w not in russian_stopwords
                    and w != " " \
                    and w.strip() not in punctuation \
                    and (re.search('\d+', w) is None) \
                    and (re.search('«', w) is None) \
                    and len(w) > 1]
    string_tokens = [morph.parse(w)[0].normal_form for w in string_words]
    return string_tokens


if __name__ == '__main__':
    print("POINT1")

    for i in range(files_len):
        file_names.append(files[i])

    file_to_terms = process_files(file_names)
    regular_index = make_indices(file_to_terms)
    total_index = fullIndex(regular_index)


    print("POINT2")


    print(strict_text_query('новости'))
    print('OR')
    print(free_text_query('новости спорт'))
    print('AND')
    print(strict_text_query('новости спорт футбол'))
    print('NOT')
    print(not_phrase_query('главные новости'))