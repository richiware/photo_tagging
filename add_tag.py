#!/usr/bin/python3

import os, sys, fnmatch
from subprocess import Popen, call, PIPE

tags = []
subject = None
filename = None
must_rename = False

def print_help():
    print('add_tag.py <options> tags')
    print('\nOptions:')
    print('\t-s: Next tag will be use as subject.')
    print('\t-r: rename filenames with subject.')
    print('\t-R: rename filenames with next parameter.')

def getArguments():
    global tags
    global subject
    global filename
    global must_rename
    expecting_filename = False
    expecting_subject = False

    for i in range(1, len(sys.argv)):
        if expecting_filename:
            if sys.argv[i].startswith('-'):
                print('\033[91merror: Unexpected option ' + sys.argv[i] + '\033[0m')
                print_help()
                sys.exit(-1)
            expecting_filename = False
            filename = sys.argv[i]
        elif expecting_subject:
            if sys.argv[i].startswith('-'):
                print('\033[91merror: Unexpected option ' + sys.argv[i] + '\033[0m')
                print_help()
                sys.exit(-1)
            expecting_subject = False
            subject = sys.argv[i]
            tags.append(sys.argv[i])
        else:
            if sys.argv[i] == "-s":
                expecting_subject = True
            elif sys.argv[i] == "-r":
                must_rename = True
            elif sys.argv[i] == "-R":
                must_rename = True
                expecting_filename = True
            elif sys.argv[i] == "-h" or sys.argv[i] == "--help":
                print_help()
                sys.exit(-1)
            elif sys.argv[i].startswith('-'):
                print('\033[91merror: Unexpected option ' + sys.argv[i] + '\033[0m')
                print_help()
                sys.exit(-1)
            else:
                tags.append(sys.argv[i])

    if expecting_filename or expecting_subject:
        print('\033[91merror: Número de parámetros erroneo\033[0m')
        print_help()
        sys.exit(-1)
    elif must_rename and not subject and not filename:
        print('\033[91merror: Parámetros erroneo\033[0m')
        print_help()
        sys.exit(-1)

def processImages():

    # Rename files
    if must_rename:
        file_name = subject
        if filename:
            file_name = filename
        call(['exiftool', '-FileName<' + file_name + ' ${DateTimeOriginal}.jpg', '-d', '%Y%m%d-%H%M%S%%-c', '-ext', 'jpg', '.'])

    for fname in os.listdir('.'):
        if fnmatch.fnmatch(fname, '*.[jJ][pP][gG]'):
            filesize_orig = os.path.getsize(fname)

            # Get previous XPKeywords
            process = Popen(['exiftool', '-exif:XPKeywords', '-ext', 'jpg', fname], stdout=PIPE)
            output, err = process.communicate()
            keywords = ""
            for line in output.splitlines():
                strline = line.decode()
                if fnmatch.fnmatch(strline, 'XP Keywords*'):
                    index = strline.index(':')
                    keywords = strline[index+2:]
                    break

            arguments = ['exiftool', '-codedcharacterset=utf8']
            if subject:
                arguments.append('-exif:XPSubject=' + subject)
                arguments.append('-xmp:Subject=' + subject)
            for tag in tags:
                arguments.append('-iptc:Keywords+=' + tag)
                if(keywords):
                    keywords = tag + ';' + keywords
                else:
                    keywords = tag
            if(keywords):
                arguments.append('-exif:XPKeywords=' + keywords)
            arguments.append('-ext')
            arguments.append('jpg')
            arguments.append(fname)

            # Añadir tags.
            call(arguments)

            # Compare early size with new
            if filesize_orig < os.path.getsize(fname):
                os.remove(fname + '_original')
            else:
                print("\033[91mPossible corruption adding tag\033[0m")

            print("Added tag \033[95m" + ','.join(tags) + "\033[0m")

if __name__ == "__main__":
    getArguments()
    processImages()

