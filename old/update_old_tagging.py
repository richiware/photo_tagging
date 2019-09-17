#!/usr/bin/python3

import os, sys, io, fnmatch
from subprocess import Popen, call, PIPE

tag = ""

def getArguments():
    global tag

    if(len(sys.argv) == 2):
        tag = sys.argv[1];

def processImages():
    # Select one JPG or all JPG is directory.
    for fname in os.listdir('.'):
        if fnmatch.fnmatch(fname, '*.jpg'):
            processImage(fname)

def processImage(fname):
    # Safe size of one file.
    filesize_orig = os.path.getsize(fname)

    # Get IPTC Keywords
    process = Popen(['exiftool', '-iptc:Keywords', '-ext', 'jpg', fname], stdout=PIPE)
    output, err = process.communicate()
    keywords = ""
    for line in output.splitlines():
        strline = line.decode()
        if fnmatch.fnmatch(strline, 'Keywords*'):
            index = strline.index(':')
            keywords = strline[index+2:]
            break
    # Separate keywords and remove tag
    if(keywords):
        names = keywords.split(', ')
        if tag:
            names.remove(tag)

        # For each name insert it in the metadata
        if tag:
            xpkeywords = tag
        else:
            xpkeywords = ""

        for name in names:
            # Call exiftool
            call(['exiftool', '-codedcharacterset=utf8', '-xmp:PersonInImage+=' + name, '-ext', 'jpg', fname])

            # Add XPKeywords to list.
            if(xpkeywords):
                xpkeywords = name + ';' + xpkeywords
            else:
                xpkeywords = name

        # Add XPKeywords
        if tag:
            call(['exiftool', '-codedcharacterset=utf8', '-exif:XPSubject=' + tag, '-exif:XPKeywords=' + xpkeywords,
                '-xmp:Subject=' + tag, '-ext', 'jpg', fname])
        else:
            call(['exiftool', '-codedcharacterset=utf8', '-exif:XPKeywords=' + xpkeywords,
                '-ext', 'jpg', fname])

        os.remove(fname + '_original')

if __name__ == "__main__":
    getArguments()
    processImages()
