#!/usr/bin/env python
# -*- coding: utf-8 -*-

import eyed3
from nltk.tag import pos_tag
import nltk
import os
import re

eyed3.log.setLevel("ERROR")

print "========= PRE TAG EDITING SCRIPT =========="
print "This Script iterates over a given directory and tries to pre-edit the title and the album of the mp3 files."
print "WARNING: This script could overwrite titles/ album names you have edited before."
print
directory = raw_input("Please provide the filepath to the folder in which the mp3 files should be edited: ")
# directory = "C:/Users/Sebastian/Desktop/Musik/"

# Set english vocabs
english_vocab = set(w.lower() for w in nltk.corpus.words.words())

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

version22counter = 0

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
            album = mp3.tag.album
            artist = mp3.tag.artist

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

            # edit artist
            artist = artist.replace("Feat.", "feat.")
            mp3.tag.artist = artist

            # edit album artist
            if not ("Remix" in title and "remix" in title) and (album_artist is None or album_artist is ""):
                mp3.tag.album_artist = re.split(" +feat.", artist)[0]

            # save edited tags
            mp3.tag.save()

        else:
            version22counter += 1
            print "File with ID3 V 2.2.0 Tags found: ", filepath.decode("Cp1252")

print("-----------")
print "Amount of MP3 Files with ID3 V 2.2.0: ", version22counter
