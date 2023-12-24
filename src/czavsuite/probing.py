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

"""probing functionality"""

from . import config, ffmpeg
from czutils.utils import cztext
from builtins import ValueError


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
        self._table.append([ probe["codec_name"],
                             "%sx%s" % (probe["width"], probe["height"]),
                             probe["display_aspect_ratio"],
                             probe["avg_frame_rate"],
                             file ])
    #addVideo


    def addAudio(self, file: str, probe: dict):
        try:
            bitRate = "%d kb/s" % (int(probe["bit_rate"]) / 1000)
        except ValueError:
            bitRate = probe["bit_rate"]
        #except
        self._table.append([ probe["codec_name"],
                             "%s Hz" % probe["sample_rate"],
                             probe["channel_layout"],
                             bitRate,
                             file ])
    #addVideo


    def addDuration(self, file: str, duration: str):
        self._table.append([ duration, file ])
    #addVideo

#TableMaker


def avProbe(files: list, mode: int, headers: bool):
    """
    Prints info on input files to STDOUT.
    Invalid files (non-existent or non-media files) are ignored silently.

    :param files: list of input files
    :param conf: mode:
                 config.Probing.FULL:     print full information (FFmpeg default)
                 config.Probing.VIDEO:    print only video information
                 config.Probing.AUDIO:    print only audio information
                 config.Probing.DURATION: print only duration
    """
    if mode == config.Probing.FULL:
        for file in files:
            print(cztext.colourise(file, cztext.Col16.BLUE, bold=True))
            print("\n".join(ffmpeg.ffprobe(file, mode)))
        #for
    elif mode == config.Probing.DURATION:
        tm = TableMaker()
        if headers:
            tm.addHeader(mode)
        #if
        for file in files:
            tm.addDuration(file, ffmpeg.ffprobe(file, mode))
        #for
        print(_table2String(tm.get()))
    else:
        tm = TableMaker()
        if headers:
            tm.addHeader(mode)
        #if
        for file in files:
            probe = ffmpeg.ffprobe(file, mode)
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
#probe
