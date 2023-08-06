"""
Record TermCasts

See the Flags (-h) regarding possibilities.
"""

"""

#   Original Authors: Wolfgang Richter <wolfgang.richter@gmail.com> 
#   Copyright 2014-2017 Wolfgang Richter and licensed under the MIT License. #

"""
import os, time
from functools import partial
import time, json
from devapp.tools import FLG, project, gitcmd, parse_kw_str, termsize
from devapp.app import app, run_app, system, do

# from operators.testing.auto_docs import dir_pytest_base
from devapp.tools import project, read_file, write_file
import shutil


import os
from contextlib import closing
from codecs import open as copen
from json import dumps
from math import ceil
from os.path import basename, dirname, exists, join
from os import system, environ as env
from struct import unpack
from subprocess import Popen
from sys import platform, prefix, stderr
from tempfile import NamedTemporaryFile


class Flags:
    """
    """

    autoshort = ''

    class command:
        n = 'run a command and quit. Default: bash'

    class shot:
        n = 'shot mode, json output as lines to copy'
        d = False

    class output_file:
        n = 'file to output recording to. "-" to print to stdout'
        d = './termcast.json'

    class script_file:
        n = 'script file to parse'

    class timing_file:
        n = 'timing file to parse'

    class tempfile:
        n = 'full path for tempfiles (extensions will be added)'

    class open_in_browser:
        n = 'After recording create a plain html and open in browser'
        d = False


# http://stackoverflow.com/a/8220141/3362361
def testOSX():
    return platform == 'darwin'


def escapeString(string):
    string = string.encode('unicode_escape').decode('utf-8')
    string = string.replace("'", "\\'")
    string = "'" + string + "'"
    return string


def runScript(command=None, tempfile=None):
    timingfname = None
    scriptfname = None
    CMD = ['script']

    if tempfile:
        timingfname = '%s.timing' % str(tempfile)
        scriptfname = '%s.log' % str(tempfile)
        with open(timingfname, 'w'):
            with open(scriptfname, 'w'):
                pass
    else:
        with NamedTemporaryFile(delete=False) as timingf:
            with NamedTemporaryFile(delete=False) as scriptf:
                timingfname = timingf.name
                scriptfname = scriptf.name

    CMD.append('-t')

    if command:
        CMD.append('-c')
        CMD.append(command)

    CMD.append(scriptfname)
    app.info('Starting recording', cmd=CMD)

    with open(timingfname, 'w') as timingf:
        proc = Popen(CMD, stderr=timingf)
        proc.wait()

    return (
        copen(scriptfname, encoding='utf-8', errors='replace'),
        open(timingfname, 'r'),
    )


def getTiming(timef):
    timing = None
    with closing(timef):
        timing = [l.strip().split(' ') for l in timef]
        timing = [(int(ceil(float(r[0]) * 1000)), int(r[1])) for r in timing]
    return timing


def scriptToJSON(scriptf, timing=None):
    ret = []

    with closing(scriptf):
        scriptf.readline()  # ignore first header line from script file
        offset = 0
        for t in timing:
            data = escapeString(scriptf.read(t[1]))
            offset += t[0]
            ret.append((data, offset))
    return ret


def run():

    # backend = FLG.backend
    command = FLG.command
    scriptf = FLG.script_file
    outf = FLG.output_file
    timef = FLG.timing_file
    tempfile = FLG.tempfile
    shot_mode = FLG.shot
    isOSX = testOSX()
    if not outf:
        outf = '-'
    if outf == '-' and FLG.open_in_browser:
        app.die('Require file to open in browser')
    # if backend != TTYREC and ((scriptf and not timef) or (timef and not scriptf)):
    if (scriptf and not timef) or (timef and not scriptf):
        app.die('Both SCRIPT_FILE and TIMING_FILE have to be specified together.')

    if not scriptf:
        scriptf, timef = runScript(command=command, tempfile=tempfile)
        # if backend == TTYREC:
        #     scriptf = runTtyrec(command)
        # else:
    else:
        scriptf = copen(scriptf, encoding='utf-8', errors='replace')
    timing = getTiming(timef)
    frames = scriptToJSON(scriptf, timing)
    # tcstart tcend funcitons in AXC (or via shortcut):
    f1 = []
    ts = '<-------/termcast start/------->'
    te = '<-------/termcast end/------->'
    t = '<-------/termcast '
    offs, tlen = 0, len(t) + 10  # sometimes with \\r\\n at start
    for f in frames:
        c = f[0]
        if t in c[:tlen]:
            if ts in c:
                f1 = []
                offs = f[1]
                continue
            elif te in c:
                # end - remove the entry of the end command:
                for i in range(7):
                    f1.pop()
                    if '\\n' in f1[-1][0]:
                        break
                break
        f1.append((c, f[1] - offs))
    frames = f1

    h, w = termsize()
    u = env.get('SUDO_USER', env.get('USER', 'n.a.'))
    meta = {
        'rows': h,
        'cols': w,
        'ts': time.time(),
        'kB': 0,
        'by': u,
        'cmd': command,
    }
    # gk: 3 years later: wtf?
    # if shot_mode and not outf:
    #     # for copy and paste
    #     print('please clear scrollback buffer now <CMD>-k on mac')
    #     input(' ')
    breakpoint()  # FIXME BREAKPOINT
    if shot_mode:
        frames = [i[0] for i in frames]  # timing no need
        # dump = dumps(frames, indent=2).encode('utf-8')

    frames.insert(0, meta)
    jsdump = dumps(frames, indent=2)  # .encode('utf-8')
    meta['kB'] = round(len(jsdump) / 1024, 3)

    if outf == '-':
        print(jsdump)
    else:
        write_file(outf, jsdump)
        app.info('Written %s' % outf, **meta)
        meta['filename'] = outf
        app.info('Add tag', tag='\n' + t_cast % meta + '\n')
        if FLG.open_in_browser:
            open_in_browser(frames)


t_cast = '<termcast rows="%(rows)s" cols="%(cols)s" looping play_speed="-1" src="%(filename)s" />'


def open_in_browser(frames):
    meta = frames[0]

    breakpoint()  # FIXME BREAKPOINT


main = partial(run_app, run, flags=Flags)

# old tty rec stuff (for osx):
#     class backend:
#         n = 'Use script. ttyrec only on osx - not tested'
#         t = ['script', 'ttyrec']
#         d = 'script'

# def runTtyrec(command=None):
#     scriptfname = None
#     CMD = ['ttyrec']

#     with NamedTemporaryFile(delete=False) as scriptf:
#         scriptfname = scriptf.name

#     if command:
#         CMD.append('-e')
#         CMD.append(command)

#     CMD.append(scriptfname)

#     proc = Popen(CMD)
#     proc.wait()
#     return open(scriptfname, 'rb')


# def parseTtyrec(scriptf):
#     pos = 0
#     offset = 0
#     oldtime = 0
#     ret = []

#     with closing(scriptf):
#         data = scriptf.read()
#         while pos < len(data):
#             secs, usecs, amount = unpack('iii', data[pos : pos + 12])
#             pos += 12
#             timing = int(ceil(secs * 1000 + float(usecs) / 1000))
#             if oldtime:
#                 offset += timing - oldtime
#             oldtime = timing
#             ret.append(
#                 (
#                     escapeString(
#                         data[pos : pos + amount].decode(
#                             encoding='utf-8', errors='replace'
#                         )
#                     ),
#                     offset,
#                 )
#             )
#             pos += amount
#     return ret


#     if not backend:
#         if isOSX:
#             backend = TTYREC
#         else:
#             backend = 'script'
# if backend == TTYREC:
#     scriptf = open(scriptf, 'rb')
# else:

# if backend == TTYREC:
#     frames = parseTtyrec(scriptf)
# else:
