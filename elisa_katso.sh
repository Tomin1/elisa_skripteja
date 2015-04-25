#!/bin/bash
# Public domain
TMP_FILE="/tmp/elisa-viihde-$$.mpg"
sh -c "sleep 10 && vlc $TMP_FILE" &
wget ${@: 1:${#@}-1} -O "$TMP_FILE" $(elisa_url.py "${@: -1}")
wait && rm "$TMP_FILE"