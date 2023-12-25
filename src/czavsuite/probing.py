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

"""av-probe implementation"""

from . import config, utils
from czutils.utils import cztext, czlogging
from builtins import ValueError


_logger = czlogging.LoggingChannel("czavsuite.probing",
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
    _logger = czlogging.LoggingChannel("czavsuite.probing", level, colour=colour)
#setLoggingOptions


def _ffprobeDict(lines: list):
    ans = dict()
    for line in lines:
        tokens = line.split(sep='=')
        if len(tokens) == 2:
            ans[tokens[0]] = tokens[1]
        #if
    #for
    return ans
#_ffprobeDict


def ffprobe(file: str, mode: int):
    """
    """
    S = utils.SystemCaller(True)

    if mode == config.Probing.FULL:
        returnCode = S.call(['ffprobe', '-hide_banner', file])
        _logger.info("return code:", returnCode)
        _logger.info("stdout:", S.stdout())
        _logger.info("stderr:", S.stderr())
        return utils.grep("Video|Audio",
                          utils.grep("Stream", S.stderr()),
                          colour=True)
    elif mode == config.Probing.VIDEO or mode == config.Probing.AUDIO:
        returnCode = S.call(['ffprobe', '-hide_banner',
                             '-show_streams', '-select_streams',
                             'v' if mode == config.Probing.VIDEO else 'a',
                             file])
        _logger.info("return code:", returnCode)
        _logger.info("stdout:", S.stdout())
        _logger.info("stderr:", S.stderr())
        return _ffprobeDict(S.stdout().split(sep='\n'))
    elif mode == config.Probing.DURATION:
        returnCode = S.call(['ffprobe', '-hide_banner', file])
        _logger.info("return code:", returnCode)
        _logger.info("stdout:", S.stdout())
        _logger.info("stderr:", S.stderr())
        return utils.grep("Duration", S.stderr())[0].split(sep=',')[0].split(sep=' ')[3]
    else:
        raise ValueError
    #else
#ffprobe


def _table2String(table):
    if len(table) == 0:
        raise ValueError
    #if
    widths = [ len(row) for row in table ]
    if min(widths) != max(widths):
        raise ValueError
    #if

    maxWidth = [ 0 ] * len(table[0])
    for row in table:
        maxWidth = [ max(maxWidth[i], len(row[i])) for i in range(len(row)) ]
    #for
    ans = []
    for row in table:
        ans.append([ row[i].ljust(maxWidth[i]) for i in range(len(row)) ])
    #for
    return "\n".join([ "  ".join(row) for row in ans])
#_table2String


class TableMaker:
    """
    """
    def __init__(self):
        self._table = []
    #__init__


    def get(self):
        return self._table
    #get


    def addHeader(self, mode: int):
        if mode == config.Probing.VIDEO:
            self._table.append([ "codec", "resolution", "aspect ratio", "fps", "file" ])
            self._table.append([ "-----", "----------", "------------", "---", "----" ])
        elif mode == config.Probing.AUDIO:
            self._table.append([ "codec", "sample rate", "layout", "bitrate", "file" ])
            self._table.append([ "-----", "-----------", "------", "-------", "----" ])
        elif mode == config.Probing.DURATION:
            self._table.append([ "duration", "file" ])
            self._table.append([ "--------", "----" ])
        else:
            raise ValueError
        #else
    #addHeader

    def addVideo(self, file: str, probe: dict):
        try:
            try:
                framerateTokens = probe["avg_frame_rate"].split(sep='/')
                num = float(framerateTokens[0])
                den = float(framerateTokens[1])
                framerate = str(round(num / den, 2))
            except IndexError:
                framerate = probe["avg_frame_rate"]
            except ValueError:
                framerate = probe["avg_frame_rate"]
            #except
            self._table.append([ probe["codec_name"],
                                 "%sx%s" % (probe["width"], probe["height"]),
                                 probe["display_aspect_ratio"],
                                 framerate,
                                 file ])
        except KeyError:
            self._table.append([ 'null', '--', '--', '--', file ])
        #except
    #addVideo


    def addAudio(self, file: str, probe: dict):
        try:
            try:
                bitRate = "%d kb/s" % (float(probe["bit_rate"]) / 1000)
            except ValueError:
                bitRate = probe["bit_rate"]
            #except
            self._table.append([ probe["codec_name"],
                                 "%s Hz" % probe["sample_rate"],
                                 probe["channel_layout"],
                                 bitRate,
                                 file ])
        except KeyError:
            self._table.append([ 'null', '--', '--', '--', file ])
        #except
    #addAudio


    def addDuration(self, file: str, duration: str):
        self._table.append([ duration, file ])
    #addDuration

#TableMaker


def avProbe(files: list, mode: int, headers: bool):
    """
    """
    if mode == config.Probing.FULL:
        for file in files:
            print(cztext.colourise(file, cztext.Col16.BLUE, bold=True))
            print("\n".join(ffprobe(file, mode)))
        #for
    elif mode == config.Probing.DURATION:
        tm = TableMaker()
        if headers:
            tm.addHeader(mode)
        #if
        for file in files:
            tm.addDuration(file, ffprobe(file, mode))
        #for
        print(_table2String(tm.get()))
    else:
        tm = TableMaker()
        if headers:
            tm.addHeader(mode)
        #if
        for file in files:
            probe = ffprobe(file, mode)
            if mode == config.Probing.VIDEO:
                tm.addVideo(file, probe)
            elif mode == config.Probing.AUDIO:
                tm.addAudio(file, probe)
            else:
                raise ValueError
            #else
        #for
        print(_table2String(tm.get()))
    #else
#avProbe


### aczutro ###################################################################
