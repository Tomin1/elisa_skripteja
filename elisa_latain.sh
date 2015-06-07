#!/bin/bash
# Public domain
# Requires: elisa_url.py, wget
# Use: elisa_latain.sh [arguments_to_wget] \
#          url_of_the_video_page_in_elisa_viihde video_file
URL=$(elisa_url.py "${@: -2:1}")
if [ "$?" -ne "0" ]; then
    echo "Ei voitu hakea osoitetta videolle!"
    exit 2
fi
wget ${@: 1:${#@}-2} -O "${@: -1}" "$URL"
