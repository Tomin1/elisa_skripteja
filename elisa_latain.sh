#!/bin/bash
wget ${@: 1:${#@}-2} -O "${@: -1}" $(elisa_url.py "${@: -2:1}")