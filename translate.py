import collections
import csv
import subprocess
from os import listdir
from os.path import isfile, join

import time
from google.cloud import translate

base_words_dir = './docs'
extracted_words = collections.OrderedDict()


def extract_words():
    words_docs = [f for f in listdir(base_words_dir) if isfile(join(base_words_dir, f))]
    for word_doc in words_docs:
        docs_text = subprocess. \
            check_output(['antiword', '-f', '%s/%s' % (base_words_dir, word_doc)]). \
            decode('utf-8')
        for word in [w.strip('\n').strip() for w in
                     docs_text[docs_text.find('ergänzen können.') + 16:].split('|')]:
            if len(word) > 2 and word not in extracted_words.keys():
                extracted_words[word] = ''


def translate_list():
    translate_client = translate.Client()
    target = 'en'
    source = 'de'

    for word in extracted_words.keys():
        time.sleep(.1)
        translation = translate_client.translate(word, target_language=target, source_language=source)
        extracted_words[word] = translation['translatedText']
        print('%s --- %s' % (word, extracted_words[word]))

    with open('translations.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in extracted_words.items():
            writer.writerow([key, value])


if __name__ == "__main__":
    extract_words()
    translate_list()
