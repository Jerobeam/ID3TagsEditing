#!/usr/bin/env python
# -*- coding: utf-8 -*-

import eyed3
from nltk.tag import pos_tag
import nltk
import os

# Set english vocabs
english_vocab = set(w.lower() for w in nltk.corpus.words.words())

# directory = raw_input("Please provide the filepath to the folder in which the mp3 files should be edited: ")

directory = "C:/Users/Sebastian/Desktop/Musik/"

def modify_string(str):
    str = str.replace("(", "[")
    str = str.replace(")", "]")

    # check if str is english
    if str.split()[0].lower() in english_vocab:
        tagged_sent = pos_tag(str.split())
        propernouns = [word for word, pos in tagged_sent if pos == 'NN' or pos == 'NNS' or pos == 'JJR' or pos == 'NNP']

        str = ""
        for word, pos in tagged_sent:
            if word in propernouns or 'dj' in word:
                word = word.title()

            str += word + " "

        # Delete ending whitespaces
        str = str.rstrip()
    return str

for dirName, subdirList, files in os.walk(directory, topdown=False):
    for fname in files:
        filepath = os.path.join(dirName, fname)

        if fname.lower().endswith('.mp3'):
            mp3 = eyed3.load(filepath)
        else:
            # Skip iteration for non mp3 files
            continue

        # Try to edit tags if possible (not working for ID3 V 2.2.0)
        if mp3.tag.version != (2, 2, 0):
            title = mp3.tag.title
            artist = mp3.tag.artist
            album = mp3.tag.album

            # edit title
            if title is None:
                title = u"" + os.path.splitext(fname)[0].decode("Cp1252")

            title = modify_string(title)

            mp3.tag.title = u"" + title

            # edit album
            if album is not None:
                album = modify_string(album)
                mp3.tag.album = u"" + album
            else:
                mp3.tag.album = u"" + title

            mp3.tag.save()

