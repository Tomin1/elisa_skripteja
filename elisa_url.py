#!/usr/bin/env python3
# 
# Elisa Viihde url hakija
# Copyright (c) Tomi Leppänen, 2014-2015
# 

from http.cookiejar import CookieJar
from urllib.request import urlopen, build_opener, HTTPCookieProcessor
from urllib.parse import urlencode, urlparse, parse_qsl
from json import loads as json_loads
from re import compile as re_compile

USERNAME='laita käyttäjä tähän'
PASSWORD='laita salasana tähän'

BASE_URL = "http://api.elisaviihde.fi/etvrecorder/"
LOGIN_URL = BASE_URL + "login.sl"
PROGRAM_INFO_URL = BASE_URL + "program.sl"
PROGRAM_VIDEO_PAGE_REGEX = re_compile(
    r"https?://elisaviihde.fi/tallenteet/katso/(?P<id>\d+)"
)
PROGRAM_INFO_PAGE_REGEX = re_compile(
    r"https?://elisaviihde.fi/ohjelmaopas/ohjelma/(?P<id>\d+)"
)

def login(username, password):
    cookies = CookieJar()
    opener = build_opener(HTTPCookieProcessor(cookies))
    response = opener.open(LOGIN_URL, data=urlencode({
            'username': username, 
            'password': password, 
            'savelogin': None, 
            'ajax': True, 
        }).encode('utf-8')
    )
    if response.read() != b"TRUE":
        return None
    return cookies

def get_programid(string):
    try:
        value = int(string)
    except ValueError:
        pass
    else:
        return value
    m = PROGRAM_VIDEO_PAGE_REGEX.match(string)
    if m is None:
        m = PROGRAM_INFO_PAGE_REGEX.match(string)
    if m is None:
        return None
    return int(m.group("id"))

def get_program_info(login, programid):
    opener = build_opener(HTTPCookieProcessor(login))
    response = opener.open(PROGRAM_INFO_URL, data=urlencode({
            'programid': programid, 
            'ajax': True, 
        }).encode('utf-8')
    )
    try:
        data = json_loads(response.read().decode('utf-8'))
    except ValueError:
        return None
    return data

def main(prog=None, program=None):
    from sys import stderr
    creds = login(USERNAME, PASSWORD)
    if creds is None:
        stderr.write("Login was not successful!\n")
        return 2
    if program is None:
        stderr.write("Type program id or url: ")
        program = input("Type program id or url: ")
    programid = get_programid(program)
    if programid is None:
        stderr.write("Invalid program id or url!\n")
        return 3
    program_info = get_program_info(creds, programid)
    print(program_info['url'], end='')
    return 0

if __name__ == '__main__':
    from sys import argv
    main(*argv)