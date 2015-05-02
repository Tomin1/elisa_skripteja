#!/bin/bash
# Public domain
# Requires: elisa_url.py, vlc, wget
# Recommends: inotifywait (inotify-tools)
# Use: elisa_katso.sh url_of_the_video_page_in_elisa_viihde
TMP_FILE="/tmp/elisa-viihde-$$.mpg"
#TMP_FILE="$HOME/.cache/elisa-viihde-$$.mpg"
URL=$(elisa_url.py "${@: -1}")
if [ "$?" -ne "0" ]; then
    echo "Ei voitu hakea osoitetta videolle!"
    exit 2
fi
if [ -z $(which inotifywait 2> /dev/null) ]; then
    sh -c "sleep 10 && vlc $TMP_FILE" &
else
    sh -c "inotifywait -e create --include $TMP_FILE ${TMP_FILE%/*} && vlc $TMP_FILE" &
    sleep 1
fi
wget ${@: 1:${#@}-1} -O "$TMP_FILE" "$URL"
wait && rm "$TMP_FILE"