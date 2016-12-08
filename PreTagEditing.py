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
print "==========================================="
print
# directory = "C:/Users/Sebastian/Desktop/Testmusik/"

# Set english vocabs
english_vocab = set(w.lower() for w in nltk.corpus.words.words())

def replace_string(str):
    # Replace certain symbols
    str = str.replace("(", "[")
    str = str.replace(")", "]")
    # Delete certain string occurences
    str = str.replace("[Explicit]", "")
    str = str.replace("[explicit]", "")
    str = str.replace("[Explicit Album Version]", "")
    str = str.replace("[explicit Album Version]", "")
    str = str.replace("[explicit album Version]", "")
    str = str.replace("[Datpiff Exclusive]", "")
    str = str.replace("[datpiff Exclusive]", "")
    str = str.replace("[DatPiff Exclusive]", "")
    str = str.replace("- single", "")
    str = str.replace("- Single", "")
    # Replace wrong artist occurences
    str = str. replace("Schoolboy Q", "ScHoolBoy Q")
    str = str. replace("SchoolBoy Q", "ScHoolBoy Q")
    str = str. replace("ScHoolboy Q", "ScHoolBoy Q")
    str = str.replace("CHIEF KEEF", "Chief Keef")
    # Replace wrong "Remix" occurences
    str = str.replace("remix", "Remix")
    str = str.replace("RMX", "Remix")
    str = str.replace("rmx", "Remix")
    # Replace wrong "feat." occurences
    str = str.replace("feat", "feat.")
    str = str.replace("Feat", "feat.")
    str = str.replace(" ft", " feat.")
    str = str.replace(" Ft", " feat.")
    str = str.replace("Feat.", "feat.")
    str = str.replace("ft.", "feat.")
    str = str.replace("Ft.", "feat.")
    str = str.replace("feat..", "feat.")
    str = str.replace("Feat..", "feat.")
    str = str.replace("ft..", "feat.")
    str = str.replace("Ft..", "feat.")
    # English fixes
    str = str.replace("Dont", "Don't")
    str = str.replace("dont", "don't")
    str = str.replace("Aint", "Ain't")
    str = str.replace("aint", "ain't")
    str = str.replace("Thats", "That's")
    str = str.replace("thats", "that's")
    str = str.replace("swag", "Swag")
    str = str.replace("i'm", "I'm")
    # Replace Prod to delete it afterwards
    str = str.replace("[prod", "[Prod")
    str = str.replace("prod ", "[Prod ")
    str = str.replace("PROD ", "[Prod ")
    str = str.replace("Prod ", "[Prod ")
    if "[Prod" in str:
        str = str.split("[Prod")[0]

    str = str.strip()

    return str

def capitalize_nouns(str):
    # check if str is english
    stringLength = len(str.split());
    if stringLength > 1:
        isEnglish = (str.split()[0].lower() in english_vocab) or (str.split()[1].lower() in english_vocab)
    else:
        isEnglish = (str.split()[0].lower() in english_vocab)

    if isEnglish:
    # if False:
        str = str.lower()
        str = str.capitalize()
        tagged_sent = pos_tag(str.split())
        propernouns = [word for word, pos in tagged_sent if pos == 'NN' or pos == 'NNS' or pos == 'JJR']

        str = ""
        for word, pos in tagged_sent:
            if word in propernouns or 'dj' in word:
                word = word.title()

            str += word + " "

    str = replace_string(str)

    return str

def extract_artist_parts(str):
    if "feat." in str:
        artistPt = str.split("feat.")[1]
        if "Remix" in artistPt:
            artistPt = artistPt.split("Remix")[0]
        if "[" in artistPt:
            artistPt = artistPt.split("[")[0]
        if "]" in artistPt:
            artistPt = artistPt.split("]")[0]

        artistPt = artistPt.strip()
        return artistPt

def remove_artist_parts(str):
    if "feat." in str:
        artistPt = extract_artist_parts(str)
        if " feat." in str:
            str = str.replace(" feat. " + artistPt, "")
        if "[feat. " in str:
            str = str.replace(" [feat. " + artistPt + "]", "")

    str = str.strip()
    return str

def append_aritst_parts(artist, artistPt):
    if artistPt is not None:
        if "feat." in artist:
            if "&" not in artistPt:
                artist = artist + " & " + artistPt
            else:
                artist = artist + ", " + artistPt
        else:
            artist = artist + " feat. " + artistPt

    artist = artist.strip()
    return artist

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
            ####################
            # extract tag values
            ####################
            oldTitle = mp3.tag.title
            oldAlbum = mp3.tag.album
            oldArtist = mp3.tag.artist
            album_artist = mp3.tag.album_artist

            ####################
            # set values
            ####################
            # set title if not set
            if oldTitle is None:
                newTitle = u"" + os.path.splitext(fname)[0].decode("Cp1252")
            else:
                newTitle = oldTitle
            # set album if not set
            if oldAlbum is None or oldAlbum == "":
                newAlbum = newTitle
            else:
                newAlbum = oldAlbum
            # set album artist
            if not ("Remix" in newTitle) and (album_artist is None or album_artist is ""):
                mp3.tag.album_artist = re.split(" +feat.", newArtist)[0]

            ####################
            # replace certain values
            ####################
            newTitle = replace_string(newTitle)
            newAlbum = replace_string(oldAlbum)
            newArtist = replace_string(oldArtist)

            ####################
            # extract & remove featurings and append them to artist
            ####################
            artistPt = extract_artist_parts(newTitle)
            newTitle = remove_artist_parts(newTitle)
            newArtist = append_aritst_parts(newArtist, artistPt)
            newAlbum = remove_artist_parts(newAlbum)

            ####################
            # capitalize values
            ####################
            newTitle = capitalize_nouns(newTitle)
            newAlbum = capitalize_nouns(newAlbum)

            ####################
            # assign new tag values
            ####################
            mp3.tag.title = u"" + newTitle
            mp3.tag.album = u"" + newAlbum
            mp3.tag.artist = newArtist

            ####################
            # save edited tags
            ####################
            mp3.tag.save()

            ####################
            # log results
            ####################
            print "Old Title: ", oldTitle
            print "New Title: ", newTitle
            print "Old Artist: ", oldArtist
            print "New Artist: ", newArtist
            print "Old Album: ", oldAlbum
            print "New Album: ", newAlbum
        else:
            version22counter += 1
            print "File with ID3 V 2.2.0 Tags found: ", filepath.decode("Cp1252")

        print "_____________________"

print("---------------------")
print "Amount of MP3 Files with ID3 V 2.2.0: ", version22counter
