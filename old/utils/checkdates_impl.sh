#!/bin/bash

# Check if contains Date/Time
datetime=$(exiftool -DateTimeOriginal $1 2>/dev/null | wc -l)

if [ $datetime -lt 1 ]; then
    # Try to set using the filename.
    first=$(echo $1 | awk -F '[^[:digit:]]*' '1 {print $2}')

    if [ -n $first ]; then
        second=$(echo $1 | awk -F '[^[:digit:]]*' '1 {print $3}')

        if [ -n $second ]; then
            year=$(echo $first | awk -F '' '1 {print $1$2$3$4}')

            if [ -n $year ]; then
                month=$(echo $first | awk -F '' '1 {print $5$6}')

                if [ -n $month ]; then
                    day=$(echo $first | awk -F '' '1 {print $7$8}')

                    if [ -n $day ]; then
                        hour=$(echo $second | awk -F '' '1 {print $1$2}')

                        if [ -n $hour ]; then
                            minutes=$(echo $second | awk -F '' '1 {print $3$4}')

                            if [ -n $minutes ]; then
                                seconds=$(echo $second | awk -F '' '1 {print $5$6}')

                                if [ -n $seconds ]; then
                                    SIZEFILE_ORIG=$(stat -c '%s' "$1")
                                    exiftool -DateTimeOriginal="$year:$month:$day $hour:$minutes:$seconds" $1
                                    SIZEFILE_NEW=$(stat -c '%s' "$1")

                                    if [ $SIZEFILE_ORIG -lt $SIZEFILE_NEW ]; then
                                        echo "Added DateTime $year:$month:$day-$hour:$minutes:$seconds"
                                        rm $1_original
                                    else
                                        echo "Possible corruption adding Date/Time"
                                    fi

                                    exit 0
                                fi
                            fi
                        fi
                    fi
                fi
            fi
        fi
    fi

    echo No Date/Time in $1
fi

