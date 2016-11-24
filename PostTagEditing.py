#!/usr/bin/env python
# -*- coding: utf-8 -*-

import eyed3
from tinytag import TinyTag
import os
import re

errorcounter = 0
retitledcounter = 0

# directory = raw_input("Please provide the filepath to the folder, you want to restructure: ")

directory = "C:/Users/Sebastian/Desktop/Musik/"

title = None

for dirName, subdirList, files in os.walk(directory, topdown=False):
    for fname in files:
        filepath = os.path.join(dirName, fname)

        if fname.lower().endswith('.mp3'):
            mp3 = eyed3.load(filepath)
            title = mp3.tag.title
            artist = mp3.tag.artist
            album = mp3.tag.album
            genre = mp3.tag.genre
            fileextension = ".mp3"

            # Try to fill title if possible (not working for ID3 V 2.2.0)
            if mp3.tag.version != (2, 2, 0):
                if title is None:
                    mp3.tag.title = u"" + os.path.splitext(fname)[0].decode("Cp1252")
                    title = mp3.tag.title
                    mp3.tag.save()
                    retitledcounter += 0
                    print("Retitled: " + fname.decode("Cp1252"))

        elif fname.lower().endswith('.m4a'):
            m4a = TinyTag.get(filepath)
            title = m4a.title
            artist = m4a.artist
            album = m4a.album
            fileextension = ".m4a"

        if artist is None:
            print("Error: No artist for Song " + os.path.splitext(fname)[0].decode("Cp1252") + ".")
            errorcounter += 1
        if album is None:
            print("Error: No album for Song " + os.path.splitext(fname)[0].decode("Cp1252") + ".")
            errorcounter += 1
        else:
            # Only regard first artist (don't regard featurings)
            artist = re.split(" +feat.", artist)[0]

            if not os.path.exists(directory + artist + "/" + album):
                os.makedirs(directory + artist + "/" + album)

        # if title != os.path.splitext(fname)[0] and title is not None:
        #     newFileName = filename

        if title is None:
            print("Error: No title for Song " + os.path.splitext(fname)[0].decode("Cp1252") + ".")
            errorcounter += 1
            title = os.path.splitext(fname)[0].decode("Cp1252")

        if artist is not None and album is not None:

            movePath = directory + artist + "\\" + album + "\\" + title + fileextension

            # Only move file when they are not in the right place
            if not movePath == filepath:
                # Check if destination file already exists
                if not os.path.isfile(movePath):
                    os.rename(filepath, movePath)
                else:
                    print("Error: File " + movePath + " already existing.")
                    errorcounter += 1

    # Remove directories without any content
    if not files and not subdirList:
        os.rmdir(dirName)

print("-----------")
print("Amount of errors: ", errorcounter)
print("Amount of retitlemend: ", retitledcounter)

# For later purpose: Set album cover
# imagedata = open("D:\Bilder\Saved Pictures\Just do it Shia.jpg","rb").read()
# audiofile.tag.images.set(3, imagedata,"image/jpeg")
# audiofile.tag.save()