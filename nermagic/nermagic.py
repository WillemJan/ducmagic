#!/usr/bin/env python

import ducmagic
import torch
import multiprocessing

from pprint import pprint

from flair.data import Sentence

db = ducmagic.load()

MIN_FILESIZE = 1000  # 1 Kb
MAX_FILESIZE = 1000000  # 1 Mb

known_filetype = set()

wanted_files = {'text/plain': set(),}

from flair.models import SequenceTagger
tagger = SequenceTagger.load("flair/ner-dutch-large")

class FileProcessor:
    def __init__(self):
        pass


    def do_text(self, file):
        global tagger

        with open(file, 'r', encoding='utf-8') as file_handler:
            sentence = Sentence(file_handler.read())
            tagger.predict(sentence)
            for entity in sentence.get_spans('ner'):
                print(entity)


if __name__ == '__main__':
    for path in db:
        for file_type in db.get(path):
            if file_type in wanted_files:
                for (filename, file_size) in db[path][file_type]:
                    if file_size > MIN_FILESIZE and file_size < MAX_FILESIZE:
                        wanted_files[file_type].add(filename)
            known_filetype.add(file_type)

    proc = FileProcessor()
    ctx = multiprocessing.get_context('spawn')
    with multiprocessing.pool.Pool(1, context=ctx) as pool:
        result = pool.map(proc.do_text, wanted_files['text/plain'])
