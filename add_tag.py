#!/usr/bin/python3

import os, sys, fnmatch
from subprocess import Popen, call, PIPE

filename = ""
tagname = ""

def getArguments():
    global filename
    global tagname

    argslen = len(sys.argv)
    if argslen < 2:
        print('\033[91mERROR: Número de parámetros erroneo\033[0m')
        print('Uso: photoTag.py <filename> [tagname]')
        sys.exit(-1)
    elif argslen == 2:
        filename = sys.argv[1]
        tagname = sys.argv[1]
    else:
        filename = sys.argv[1]
        tagname = sys.argv[2]

def processImages():
    # Rename files
    call(['exiftool', '-FileName<' + filename + ' ${DateTimeOriginal}.jpg', '-d', '%Y%m%d-%H%M%S%%-c', '-ext', 'jpg', '.'])

    for fname in os.listdir('.'):
        if fnmatch.fnmatch(fname, '*.jpg'):
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
            if(keywords):
                keywords = tagname + ';' + keywords
            else:
                keywords = tagname

            # Añadir tags.
            call(['exiftool', '-codedcharacterset=utf8', '-exif:XPSubject=' + tagname, '-exif:XPKeywords=' + keywords, '-iptc:Keywords+=' + tagname, '-xmp:Subject=' + tagname, '-ext', 'jpg', fname])

            # Compare early size with new
            if filesize_orig < os.path.getsize(fname):
                print("Added tag \033[95m" + tagname + "\033[0m")
                os.remove(fname + '_original')
            else:
                print("\033[91mPossible corruption adding tag\033[0m")

if __name__ == "__main__":
    getArguments()
    processImages()

