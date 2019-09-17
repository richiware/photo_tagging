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

    # Get previous XPKeywords, Keywords and PersonInImage.
    process = Popen(['exiftool', '-ext', 'jpg', fname], stdout=PIPE)
    output, err = process.communicate()
    xpkeywords = []
    keywords = []
    persons = []
    for line in output.splitlines():
        strline = line.decode()
        if fnmatch.fnmatch(strline, 'XP Keywords*'):
            index = strline.index(':')
            xpkeywords = strline[index+2:].split(';')
        elif fnmatch.fnmatch(strline, 'Keywords*'):
            index = strline.index(':')
            keywords = strline[index+2:].split(', ')
        elif fnmatch.fnmatch(strline, 'Person In Image*'):
            index = strline.index(':')
            persons = strline[index+2:].split(', ')

    # Join keywords and people removing desired ones and make uniques using a Set.
    set_keywords = (set(xpkeywords) | set(keywords))
    set_keywords.discard('')
    set_persons = set(persons)
    set_persons.discard('')
    for name in names:
        set_keywords.discard(name)
        set_persons.discard(name)

    # Remove previos IPTC Keyworks. Otherwise new keywords will be appended and there will be duplicate keywords.
    arguments = ['exiftool', '-codedcharacterset=utf8', '-iptc:Keywords=', '-ext', 'jpg', fname]
    call(arguments)

    # Store new information.
    arguments = ['exiftool', '-codedcharacterset=utf8']
    ch_plus = ''
    for kw in set_keywords:
        arguments.append('-iptc:Keywords' + ch_plus + '=' + kw)
        ch_plus = '+'
    arguments.append('-exif:XPKeywords=' + ';'.join(set_keywords))
    arguments.append('-xmp:PersonInImage=' + ', '.join(set_persons))
    arguments.append('-ext')
    arguments.append('jpg')
    arguments.append(fname)

    call(arguments)

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
