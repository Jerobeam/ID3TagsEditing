# encoding: Cp1252

import eyed3
from tinytag import TinyTag
import os
import re

eyed3.log.setLevel("ERROR")

print "========= POST TAG EDITING SCRIPT =========="
print "This Script iterates over a given directory and structures mp3 and m4a files like directory/artist/album/song"
print "WARNING: This script deletes album covers found by iTunes."
print
directory = raw_input("Please provide the filepath to the folder, you want to restructure: ")
print "============================================"
print
# directory = "C:/Users/Sebastian/Desktop/Testmusik/"

errorcounter = 0
notitlecounter = 0
retitledcounter = 0

title = None

def modify_string(str):
    str = str.replace("/", "_")
    str = str.replace("\\", "_")
    str = str.replace(":", "")
    str = str.replace("\"", "")
    str = str.replace("drei ???", "drei Fragezeichen")
    str = str.replace("?", "")
    str = str.replace("<", "")
    str = str.replace(">", "")
    str = str.replace("*", "_")
    str = str.replace("|", "_")
    str = str.strip()
    return str

for dirName, subdirList, files in os.walk(directory, topdown=False):
    for fname in files:
        filepath = os.path.join(dirName, fname)

        if fname.lower().endswith('.mp3'):
            mp3 = eyed3.load(filepath)
            title = mp3.tag.title
            artist = mp3.tag.artist
            album = mp3.tag.album
            genre = mp3.tag.genre
            album_artist = mp3.tag.album_artist
            fileextension = ".mp3"

            # Try to fill title if possible (not working for ID3 V 2.2.0)
            if mp3.tag.version != (2, 2, 0):
                if title is None or title == "":
                    mp3.tag.title = u"" + os.path.splitext(fname)[0].decode("Cp1252")
                    title = mp3.tag.title
                    retitledcounter += 1
                    print("Retitled: " + fname.decode("Cp1252"))

                # edit album artist
                if not("Remix" in title and "remix" in title) and (album_artist is None or album_artist is ""):
                    if  artist is not None:
                        mp3.tag.album_artist = re.split(" +feat.", artist)[0]

                mp3.tag.save()
                print mp3._tag._chapters._fs

        elif fname.lower().endswith('.m4a'):
            m4a = TinyTag.get(filepath)
            title = m4a.title
            artist = m4a.artist
            album = m4a.album
            fileextension = ".m4a"
        else:
            continue

        if artist is None:
            print("ERROR: No artist for Song " + os.path.splitext(fname)[0].decode("Cp1252") + ".")
            errorcounter += 1
        else:
            # Only regard first artist (don't regard featurings)
            artist = re.split(" +feat.", artist)[0]
            artist = modify_string(artist)

        if album is None:
            print("ERROR: No album for Song " + os.path.splitext(fname)[0].decode("Cp1252") + ".")
            errorcounter += 1
        else:
            album = modify_string(album)

        if title is None:
            print("WARNING: No title for Song " + os.path.splitext(fname)[0].decode("Cp1252") + ". Using filename.")
            notitlecounter += 1
            title = os.path.splitext(fname)[0].decode("Cp1252")
        else:
            title = modify_string(title)

        if artist is not None and album is not None:

            if not os.path.exists(directory + "\\" + artist + "\\" + album):
                os.makedirs(directory + "\\" + artist + "\\" + album)

            movePath = directory + "\\" + artist + "\\" + album + "\\" + title + fileextension

            print "___________"
            print filepath
            print movePath

            # Only move file when they are not in the right place
            if not movePath == filepath.decode("Cp1252"):
                # Check if destination file already exists
                if not os.path.isfile(movePath):
                    os.rename(filepath, movePath)
                else:
                    print("ERROR: File " + movePath + " already existing.")
                    errorcounter += 1

    # Remove directories without any content
    if not files and not subdirList:
        os.rmdir(dirName)

print "-----------"
print "Amount of errors: ", errorcounter
print "Amount of retitlements: ", retitledcounter
print "Amount of songs without a title: ", notitlecounter

# For later purpose: Set album cover
# imagedata = open("D:\Bilder\Saved Pictures\Just do it Shia.jpg","rb").read()
# audiofile.tag.images.set(3, imagedata,"image/jpeg")
# audiofile.tag.save()