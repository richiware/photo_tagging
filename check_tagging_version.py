#!/usr/bin/python3

import os, sys, io, fnmatch
from subprocess import Popen, call, PIPE

debug = False

def getArguments():
    global debug

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-d":
            debug = True

def processImages():
    total = 0
    failed = 0
    # Select one JPG or all JPG is directory.
    for fname in os.listdir('.'):
        if fnmatch.fnmatch(fname, '*.jpg'):
            total += 1
            if not processImage(fname):
                failed += 1

    print("\033[94mFinished checking for " + str(total) + " files. Result:\033[0m")
    if failed > 0:
        print("\033[91mFailed " + str(failed) + " files. Could be old tagging\033[0m")
    else:
        print("\033[94mFiles have new tagging\033[0m")


def processImage(fname):
    # Prepare XPKeywords
    process = Popen(['exiftool', '-exif:XPKeywords', '-iptc:Keywords', '-ext', 'jpg', fname], stdout=PIPE)
    output, err = process.communicate()
    xpkeywords = []
    keywords = []
    for line in output.splitlines():
        strline = line.decode()
        if fnmatch.fnmatch(strline, 'XP Keywords*'):
            index = strline.index(':')
            xpkeywords = strline[index+2:].split(';')
        elif fnmatch.fnmatch(strline, 'Keywords*'):
            index = strline.index(':')
            keywords = strline[index+2:].split(', ')

    if len(xpkeywords) != len(keywords):
        if debug:
            print("\033[91mNot same number of tags in XPKeywords and Keywords ("  + fname + ")\033[0m")
            print("\033[91m\tXPKeywords = " + ','.join(xpkeywords) + "\033[0m")
            print("\033[91m\tKeywords = " + ','.join(keywords) + "\033[0m")
        return False

    set_xpkeywords = set(xpkeywords)
    set_keywords = set(keywords)

    if len(set_xpkeywords) != len(xpkeywords):
        if debug:
            print("\033[91mNot unique tags in XPKeywords ("  + fname + ")\033[0m")
            print("\033[91m\tXPKeywords = " + ','.join(xpkeywords) + "\033[0m")
        return False

    if len(set_keywords) != len(keywords):
        if debug:
            print("\033[91mNot unique tags in Keywords ("  + fname + ")\033[0m")
            print("\033[91m\tKeywords = " + ','.join(keywords) + "\033[0m")
        return False


    if len(set_xpkeywords & set_keywords) != len(set_xpkeywords):
        if debug:
            print("\033[91mNot same XPKeywords and Keywords\ ("  + fname + ")\033[0m")
            print("\033[91m\tXPKeywords = " + ','.join(xpkeywords) + "\033[0m")
            print("\033[91m\tKeywords = " + ','.join(keywords) + "\033[0m")
        return False

    return True

if __name__ == "__main__":
    getArguments()
    processImages()
