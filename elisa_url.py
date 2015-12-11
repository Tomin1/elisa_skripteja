#!/usr/bin/env python3
# 
# Elisa Viihde url hakija
# Copyright (c) Tomi Leppänen, 2014-2015
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 

from elisaviihde import elisaviihde as ElisaViihde
from re import compile as re_compile
from argparse import ArgumentParser

USERNAME='laita käyttäjä tähän'
PASSWORD='laita salasana tähän'

PROGRAM_VIDEO_PAGE_REGEX = re_compile(
    r"https?://elisaviihde.fi/tallenteet/katso/(?P<id>\d+)"
)
PROGRAM_INFO_PAGE_REGEX = re_compile(
    r"https?://elisaviihde.fi/ohjelmaopas/ohjelma/(?P<id>\d+)"
)
DIR_PAGE_REGEX = re_compile(
        r"https?://elisaviihde.fi/tallenteet/kansio/(?P<id>\d+)(?:/sivu/\d+)?"
)

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

def get_dirid(string):
    try:
        value = int(string)
    except ValueError:
        pass
    else:
        return value
    m = DIR_PAGE_REGEX.match(string)
    if m is None:
        return None
    return int(m.group("id"))

def main(prog, *arguments):
    from sys import stderr
    parser = ArgumentParser(prog=prog,
            description="Fetches video urls from Elisa Viihde.", epilog="""
You can use arguments -u, -d, -c and -t to choose what information is returned
and in which order. The default is to print only urls.""")
    parser.add_argument('program', nargs='?', help="program id or url")
    parser.add_argument('-D', '--dir', dest='directory', action='store_true',
            help="""given id or url is for a directory,
returns urls for all videos in the directory""")
    parser.add_argument('-u', '--url', dest='parts', action='append_const',
            const='url', help="print video download url")
    parser.add_argument('-i', '--id', dest='parts', action='append_const',
            const='id', help="print program id")
    parser.add_argument('-d', '--desc', dest='parts', action='append_const',
            const='description', help="print description")
    parser.add_argument('-c', '--channel', dest='parts', action='append_const',
            const='channel', help="print channel name")
    parser.add_argument('-t', '--time', dest='parts', action='append_const',
            const='time', help="print date and time")
    parser.add_argument('--debug', default=False, action='store_true',
            help="print debug information")
    args = parser.parse_args(arguments)
    elisaviihde = ElisaViihde(args.debug)
    elisaviihde.login(USERNAME, PASSWORD)
    if not elisaviihde.islogged():
        stderr.write("Login was not successful!\n")
        return 2
    if args.program is not None:
        program = args.program
    else:
        stderr.write("No program id given. Type program id or url: ")
        program = input()

    if args.directory:
        dirid = get_dirid(program)
        if dirid is None:
            stderr.write("Invalid directory id or url!\n")
            return 3
        progs = []
        page = 1
        new_progs = ["new"]
        while len(new_progs) > 0:
            try:
                new_progs = elisaviihde.getrecordings(dirid, page)
            except Exception:
                stderr.write(
"Could not fetch recordings! The id or url might be invalid!"
                )
                if args.debug:
                    stderr.write("Exception: {} \n".format(str(error)))
                return 4
            progs.extend(new_progs)
            page += 1
        if args.parts is None:
            args.parts = ['id']
        for prog in progs:
            for part in args.parts:
                if part == 'url':
                    try:
                        url = elisaviihde.getstreamuri(prog['programId'])
                    except Exception as error:
                        stderr.write(""""Can't get program url for id {}! \
Maybe the recording is not available!\n""".format(prog["programId"]))
                        if args.debug:
                            stderr.write("Exception: {} \n".format(str(error)))
                    else:
                        print('"' + url + '"', end='')
                elif part == 'id':
                    print(prog['programId'], end='')
                elif part == 'description':
                    if 'description' in prog:
                        print('"' + prog['description'] + '"', end='')
                    else:
                        print('""', end='')
                elif part == 'channel':
                    print('"' + prog['channel'] + '"', end='')
                elif part == 'time':
                    print('"' + prog['startTime'] + '"', end='')
                print(" ", end='')
            print()
    else:
        programid = get_programid(program)
        if programid is None:
            stderr.write("Invalid program id or url!\n")
            return 3
        try:
            programurl = elisaviihde.getstreamuri(programid)
        except Exception as error:
            stderr.write(
                "Can't get program url! Maybe the recording is not available!\n"
            )
            if args.debug:
                stderr.write("Exception: {} \n".format(str(error)))
            return 4
        print(programurl, end='')
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(*sys.argv))
