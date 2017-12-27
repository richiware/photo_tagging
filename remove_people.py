#!/usr/bin/python3

import os, sys, io, fnmatch
from subprocess import Popen, call, PIPE

lines = []

filename = ""
names = []

def readNombres():
    directory = os.path.dirname(os.path.realpath(__file__))
    nombresFilename = directory + '/Nombres.txt'
    nombresFile = io.open(nombresFilename, 'r', encoding='utf8')
    for line in nombresFile:
        lines.append(line[:-1])

def getArguments():
    global filename
    count = 1;

    if(not sys.argv[count].isdigit()):
        filename = sys.argv[count];
        count += 1

    for i in range(count, len(sys.argv)):
        names.append(lines[int(sys.argv[i]) - 1])

def processImages():
    # Select one JPG or all JPG is directory.
    if not filename:
        for fname in os.listdir('.'):
            if fnmatch.fnmatch(fname, '*.jpg'):
                processImage(fname)
    else:
        processImage(filename)

def processImage(fname):
    # Safe size of one file.
    filesize_orig = os.path.getsize(fname)

    # Prepare XPKeywords
    process = Popen(['exiftool', '-exif:XPKeywords', '-ext', 'jpg', fname], stdout=PIPE)
    output, err = process.communicate()
    keywords = ""
    for line in output.splitlines():
        strline = line.decode()
        if fnmatch.fnmatch(strline, 'XP Keywords*'):
            index = strline.index(':')
            keywords = strline[index+2:]
            break

    # For each name insert it in the metadata
    for name in names:
        # Call exiftool
        call(['exiftool', '-codedcharacterset=utf8', '-iptc:Keywords-=' + name, '-xmp:PersonInImage-=' + name, '-ext', 'jpg', fname])

        # Add XPKeywords to list.
        if(keywords):
            keywords = keywords.replace(name + ";", "")
            keywords = keywords.replace(name, "")

    # Add XPKeywords
    call(['exiftool', '-codedcharacterset=utf8', '-exif:XPKeywords=' + keywords, '-ext', 'jpg', fname])

    # Compare early size with new
    if filesize_orig >= os.path.getsize(fname):
        print("Removed names \033[95m" + ','.join(names) + "\033[0m")
        os.remove(fname + '_original')
    else:
        print("\033[91mPossible corruption adding tag\033[0m")

if __name__ == "__main__":
    readNombres()
    getArguments()
    processImages()
