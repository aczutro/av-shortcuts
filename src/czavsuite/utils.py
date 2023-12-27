# czavsuite - a suite of useful scripts to serialise FFmpeg jobs
#
# Copyright 2023 - present Alexander Czutro, github@czutro.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################### aczutro ###

"""Help functions that will later be moved to czutils lib
"""

from czutils.utils import czlogging, cztext
import os
import re
import subprocess


_logger = czlogging.LoggingChannel("czavsuite.utils",
                                   czlogging.LoggingLevel.SILENT,
                                   colour=True)

def setLoggingOptions(level: int, colour=True) -> None:
    """
    Sets this module's logging level.  If not called, the logging level is
    SILENT.

    :param level: One of the following:
                  - czlogging.LoggingLevel.INFO
                  - czlogging.LoggingLevel.WARNING
                  - czlogging.LoggingLevel.ERROR
                  - czlogging.LoggingLevel.SILENT

    :param colour: If true, use colour in log headers.
    """
    global _logger
    _logger = czlogging.LoggingChannel("czavsuite.utils", level, colour=colour)
#setLoggingOptions


class UtilsError(Exception):
    pass


class SystemCaller:

    def __init__(self, exceptionOnFailure: bool):
        self._stdout = ""
        self._stderr = ""
        self._doRaise = exceptionOnFailure
    #__init__


    def stdout(self):
        return self._stdout
    #stdout


    def stderr(self):
        return self._stderr
    #stdout


    def call(self, args: list) -> int:
        P = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = P.communicate()
        self._stdout = stdout.decode(errors="ignore")
        self._stderr = stderr.decode(errors="ignore")
        if P.returncode:
            _logger.warning("'%s'" % " ".join(args), "returned", P.returncode)
            if self._doRaise:
                raise UtilsError(self._stderr)
            #if
        #if
        return P.returncode
    #def

#SystemCaller


def grep(pattern: str, text, ignoreCase=False, colour=False):
    if type(text) is str:
        return grep(pattern, text.split(sep='\n'), ignoreCase, colour)
    #if

    flags = re.IGNORECASE if ignoreCase else 0
    matcher = re.compile(pattern, flags)
    ans = []
    for line in text:
        if colour:
            match = matcher.search(line)
            if match is not None:
                start, end = match.start(), match.end()
                ans.append("%s%s%s"
                           % (line[:start],
                              cztext.colourise(line[start:end], cztext.Col16.RED, bold=True),
                              line[end:]))
            #if
        else:
            if matcher.search(line) is not None:
                ans.append(line)
            #if
        #else
    #for
    return ans
#grep


def mkdir(path: str, p = False):
    if path == "":
        raise ValueError
    #if
    if path != os.path.sep and path[-1] == os.path.sep:
        path = path[:-1]
    #if
    try:
        os.mkdir(path)
    except FileExistsError as e:
        if not (os.path.isdir(path) and p):
            raise e
        #if
    except FileNotFoundError as e:
        parent = os.path.dirname(path)
        if p and parent != path:
            mkdir(parent, p)
            mkdir(path, p)
        else:
            raise e
        #else
    #except
#mkdir


def filenameSplit(filename: str) -> tuple:
    tokens = filename.split(sep='.')
    if len(tokens) < 2:
        return (filename, "")
    else:
        return (".".join(tokens[:-1]), tokens[-1])
    #else
#filenameSplit


def isHidden(path: str) -> bool:
    if path == "":
        raise ValueError
    #if
    a, b = os.path.split(path)
    if b == "":
        a, b = os.path.split(a)
    #if
    return len(b) and b[0] == '.'
#isHidden


### aczutro ###################################################################
