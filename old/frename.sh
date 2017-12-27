#!/bin/bash

# This script rename photos.

filename=
tagname=

if [ $# -lt 1 ]; then
    echo "ERROR: Numero de parametros erroneo"
    echo "Uso: frename.sh <filename> <tagname>"
    exit -1
fi

if [ $# -eq 1 ]; then
    filename=$1
    tagname=$1
elif [ $# -ge 2 ]; then
    filename=$1
    tagname=$2
fi

# Rename files
exiftool '-FileName<'"$filename"' ${DateTimeOriginal}.jpg' -d %Y%m%d-%H%M%S%%-c -ext jpg .

# Add IPTC keyword. Method to detect corruption.
FILE=$(find . -iname \*.jpg | sort -n | head -1)
SIZEFILE_ORIG=$(stat -c '%s' "$FILE")
exiftool -codedcharacterset=utf8 -iptc:keywords+="$tagname" -ext jpg .
SIZEFILE_NEW=$(stat -c '%s' "$FILE")

if [ $SIZEFILE_ORIG -lt $SIZEFILE_NEW ]; then
    rm *.jpg_original
else
    echo "Possible corruption renaming and adding tag."
fi

###### OLD ######

#for ARCH in *.JPG ; do
#    # Add tag.
#    iptc -a Keywords -v "$1" "$ARCH"
#    # Change de file name.
#    jhead "-n$1 %Y%m%d-%H%M%S" "$ARCH"
#done
