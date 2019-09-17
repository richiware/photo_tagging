#!/usr/bin/python3

import os, sys, io, fnmatch
from subprocess import Popen, call, PIPE

debug = False
notchange = False
change = False
lines = []

def getArguments():
    global debug
    global notchange
    global change

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-d":
            debug = True
        elif sys.argv[i] == "-n":
            notchange = True
        elif sys.argv[i] == "-y":
            change = True
        else:
            print("\033[91mBad arguments.\033[0m")

def readNombres():
    directory = os.path.dirname(os.path.realpath(__file__))
    nombresFilename = directory + '/Nombres.txt'
    nombresFile = io.open(nombresFilename, 'r', encoding='utf8')
    for line in nombresFile:
        lines.append(line[:-1])

def processImages():
    total = 0
    recovered = 0
    failed = 0
    # Select one JPG or all JPG is directory.
    for fname in os.listdir('.'):
        if fnmatch.fnmatch(fname, '*.jpg'):
            total += 1
            returned_value = processImage(fname)
            if returned_value > 0:
                failed += 1
            if returned_value > 1:
                recovered += 1

    print("\033[94mFinished checking for " + str(total) + " files. Result:\033[0m")
    if failed > 0:
        print("\033[91mRecovered " + str(recovered) + " files.\033[0m")
        print("\033[91mFailed " + str(failed) + " files.\033[0m")
    else:
        print("\033[94mFiles have new tagging\033[0m")


def processImage(fname):
    print("\033[94mProcessing file: "  + fname + "\033[0m")
    # Get previous XPKeywords, Keywords, XPSubject, Subject and PersonInImage.
    process = Popen(['exiftool', '-exif:XPKeywords', '-iptc:Keywords', '-exif:XPSubject', '-xmp:Subject',
    '-xmp:PersonInImage', '-ext', 'jpg', fname], stdout=PIPE)
    output, err = process.communicate()
    xpkeywords = []
    keywords = []
    xpsubject = ""
    subject = ""
    persons = []
    for line in output.splitlines():
        strline = line.decode()
        if fnmatch.fnmatch(strline, 'XP Keywords*'):
            index = strline.index(':')
            xpkeywords = strline[index+2:].split(';')
            if debug:
                print("\033[94m\tXPKeywords: "  + strline[index+2:] + "\033[0m")
        elif fnmatch.fnmatch(strline, 'Keywords*'):
            index = strline.index(':')
            keywords = strline[index+2:].split(', ')
            if debug:
                print("\033[94m\tKeywords: "  + strline[index+2:] + "\033[0m")
        elif fnmatch.fnmatch(strline, 'XP Subject*'):
            index = strline.index(':')
            xpsubject = strline[index+2:]
            if debug:
                print("\033[94m\tXPSubject: "  + strline[index+2:] + "\033[0m")
        elif fnmatch.fnmatch(strline, 'Subject*'):
            index = strline.index(':')
            subject = strline[index+2:]
            if debug:
                print("\033[94m\tSubject: "  + strline[index+2:] + "\033[0m")
        elif fnmatch.fnmatch(strline, 'Person In Image*'):
            index = strline.index(':')
            persons = strline[index+2:].split(', ')
            if debug:
                print("\033[94m\tPersonInImage: "  + strline[index+2:] + "\033[0m")

    returned_value = 0
    # Make uniques, removing duplicates.
    set_xpkeywords = set(xpkeywords)
    set_xpkeywords.discard('')
    set_keywords = set(keywords)
    set_keywords.discard('')
    set_persons = set(persons)
    set_persons.discard('')

    # Check if some preconditions fail.
    if len(set_xpkeywords) != len(xpkeywords):
        if debug:
            print("\033[91mNot unique tags in XPKeywords ("  + fname + ")\033[0m")
        returned_value = 1

    if len(set_keywords) != len(keywords):
        if debug:
            print("\033[91mNot unique tags in Keywords ("  + fname + ")\033[0m")
        returned_value = 1

    if len(set_xpkeywords & set_keywords) != len(set_xpkeywords) or \
        len(set_xpkeywords & set_keywords) != len(set_keywords):
        if debug:
            print("\033[91mNot same XPKeywords and Keywords\ ("  + fname + ")\033[0m")
        returned_value = 1

    if xpsubject != subject:
        if debug:
            print("\033[91mNot same XPSubject and Subject\ ("  + fname + ")\033[0m")
        returned_value = 1

    if len(set_persons) != len(persons):
        if debug:
            print("\033[91mNot unique tags in PersonInImage ("  + fname + ")\033[0m")
        returned_value = 1

    names = []

    for name in set_xpkeywords:
        if any(name in name_ for name_ in lines):
            names.append(name)

    for name in set_keywords:
        if any(name in name_ for name_ in lines):
            names.append(name)

    set_names = set(names)

    if len(set_names) != len(set_persons):
        if debug:
            print("\033[91mNot same keywords and PersonInImage ("  + fname + ")\033[0m")
        returned_value = 1

    if returned_value == 1 and notchange:
        return returned_value

    change_ = change

    if returned_value > 0 and not change_:
        while not change_:
            inch = input("Do you want to fix the photo? (y/n):")
            if inch == 'y':
                change_ = True
            elif inch == 'n':
                break

    if returned_value > 0 and change_:
        set_keywords_final = (set_xpkeywords | set_keywords)
        set_persons_final = (set_names | set_persons)
        if not xpsubject and subject:
            subject_final = subject
        elif xpsubject and not subject:
            subject_final = xpsubject
        elif xpsubject != subject:
            print("\033[91mXPSubject and Subject are different. Cannot be fixed. ("  + fname + ")\033[0m")
            return 1
        else:
            subject_final = subject

        # Remove previos IPTC Keyworks. Otherwise new keywords will be appended and there will be duplicate keywords.
        arguments = ['exiftool', '-codedcharacterset=utf8', '-iptc:Keywords=', '-ext', 'jpg', fname]
        call(arguments)

        # Store new information
        arguments = ['exiftool', '-codedcharacterset=utf8']
        if subject_final:
            arguments.append('-exif:XPSubject=' + subject_final)
            arguments.append('-xmp:Subject=' + subject_final)
        ch_plus = ''
        for kw in set_keywords_final:
            arguments.append('-iptc:Keywords' + ch_plus+ '=' + kw)
            ch_plus = '+'
        arguments.append('-exif:XPKeywords=' + ';'.join(set_keywords_final))
        arguments.append('-xmp:PersonInImage=' + ', '.join(set_persons_final))
        arguments.append('-ext')
        arguments.append('jpg')
        arguments.append(fname)

        call(arguments)

        os.remove(fname + '_original')

        returned_value = 2

    return returned_value

if __name__ == "__main__":
    getArguments()
    readNombres()
    processImages()
