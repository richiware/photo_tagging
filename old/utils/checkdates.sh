#!/bin/bash

dir="`dirname \"$0\"`"

find . -iname "*.jpg" -exec sh $dir/utils/checkdates_impl.sh {} \;

###### OLD #####
#find . -iname "*.jpg" -exec sh -c 'jhead "{}" 2>/dev/null | grep Date/Time &>/dev/null || echo No DateTime in "{}"' \;
#find . -iname "*.jpg" -exec sh -c 'exiftool -DateTimeOriginal "{}" 2>/dev/null | grep Date/Time &>/dev/null || echo No DateTime in "{}"' \;
