#!/usr/bin/python3

import os, sys, io, fnmatch
from subprocess import Popen, call, PIPE

lines = []

tagname = ""

def getArguments():
    global tagname

    argslen = len(sys.argv)
    if argslen < 2:
        print('\033[91mERROR: Número de parámetros erroneo\033[0m')
        print('Uso: removePhotoTag.py <tagname>')
        sys.exit(-1)
    elif argslen == 2:
        tagname = sys.argv[1]

def processImages():
    # Select one JPG or all JPG is directory.
    for fname in os.listdir('.'):
        if fnmatch.fnmatch(fname, '*.jpg'):
            processImage(fname)

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

    # Remove tag
    # Call exiftool
    call(['exiftool', '-codedcharacterset=utf8', '-exif:XPSubject-=' + tagname, '-iptc:Keywords-=' + tagname,
        '-xmp:Subject-=' + tagname, '-ext', 'jpg', fname])

    # Add XPKeywords to list.
    if(keywords):
        keywords = keywords.replace(tagname + ";", "")
        keywords = keywords.replace(tagname, "")

    # Add XPKeywords
    call(['exiftool', '-codedcharacterset=utf8', '-exif:XPKeywords=' + keywords, '-ext', 'jpg', fname])

    # Compare early size with new
    if filesize_orig >= os.path.getsize(fname):
        print("Removed tag \033[95m" + tagname + "\033[0m")
        os.remove(fname + '_original')
    else:
        print("\033[91mPossible corruption adding tag\033[0m")

if __name__ == "__main__":
    getArguments()
    processImages()

