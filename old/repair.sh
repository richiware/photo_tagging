#!/bin/sh

# Add IPTC keyword. Method to detect corruption.
FILE=$(find . -iname *.jpg | sort -n | head -1)
SIZEFILE_ORIG=$(stat -c '%s' "$FILE")
exiftool -exif:all= -tagsfromfile @ -all:all -unsafe -ext jpg .
SIZEFILE_NEW=$(stat -c '%s' "$FILE")

if [ $SIZEFILE_ORIG -gt $SIZEFILE_NEW ]; then
    echo "Photos repaired"
    rm *.jpg_original
else
    echo "Possible corruption adding tag."
fi
