#!/bin/sh

dir="`dirname \"$0\"`"
file=

printf "%d" "$1" >/dev/null 2>&1
if ! [ $? == 0 ]; then
    file=$1
    shift # Move to next parameter
    echo "Processing file: $file"

    if ! [ -f "$file" ]; then
        echo -e "\e[1;31mError:\e[0;31m The file not exists.\e[0m"
        exit -1
    fi
fi

while (( "$#" )); do
    #name=$(cat "$dir/Nombres.txt" | head -$1 | tail -1 | cut -f2- -d" " )
    name=$(cat "$dir/Nombres.txt" | head -$1 | tail -1)

    if [ -z "$file" ]; then
        # Add IPTC keyword. Method to detect corruption.
        file=$(find . -iname \*.jpg | sort -n | head -1)
        SIZEFILE_ORIG=$(stat -c '%s' "$file")
        exiftool -codedcharacterset=utf8 -iptc:keywords+="$name" -ext jpg .
        SIZEFILE_NEW=$(stat -c '%s' "$file")

        if [ $SIZEFILE_ORIG -lt $SIZEFILE_NEW ]; then
            echo "Added $name"
            rm *_original
        else
            echo "Possible corruption adding tag."
        fi
    else
        # Add IPTC keyword. Method to detect corruption.
        SIZEFILE_ORIG=$(stat -c '%s' "$file")
        exiftool -codedcharacterset=utf8 -iptc:keywords+="$name" -ext jpg "$file"
        SIZEFILE_NEW=$(stat -c '%s' "$file")

        if [ $SIZEFILE_ORIG -lt $SIZEFILE_NEW ]; then
            echo "Added $name"
            rm *_original
        else
            echo "Possible corruption adding tag."
        fi
    fi

    shift
done
