# czavsuite - a suite of useful scripts to serialise FFmpeg jobs
#
# Copyright 2020 - present Alexander Czutro, github@czutro.ch
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

"""data structures to hold settings"""

from czutils.utils import czcode


class ConfigType:
    """"Enum class" for config types.
    """
    GENERAL, VIDEO, AUDIO, \
        CROPPING, SCALING, CUTTING, \
        PROBING, SCRIPT, CLASSIFY, RENAME = range(10)
#ConfigType


@czcode.autoStr
class General:
    def __init__(self):
        self.dry = False
    #__init
#General


@czcode.autoStr
class Video:
    def __init__(self):
        self.codec = "h265"
        self.crf = "23"
        self.fps = "30"
    #__init
#Video


@czcode.autoStr
class Audio:
    def __init__(self):
        self.codec = "aac"
        self.bitrate = "256k"
        self.quality = "0"
    #__init
#Audio


@czcode.autoStr
class Cropping:
    def __init__(self):
        self.valid = False # if true, was given in the command line
        self.left = 0
        self.right = 0
        self.up = 0
        self.down = 0
    #__init
#Cropping


@czcode.autoStr
class Scaling:
    def __init__(self):
        self.valid = False # if true, was given in the command line
        self.factor = 1.0
    #__init
#Scaling


@czcode.autoStr
class Cutting:
    def __init__(self):
        self.valid = False # if true, was given in the command line
        self.start = 0.0
        self.end = 1.0
    #__init
#Cutting


@czcode.autoStr
class Probing:
    FULL, VIDEO, AUDIO, DURATION = range(4)

    def __init__(self):
        self.headers = False
        self.mode = Probing.FULL
    #__init
#Probing


@czcode.autoStr
class Script:
    def __init__(self):
        self.dry = False
        self.wilma = ".wilma"
        self.betty = ".betty"
        self.tTemplate = False
        self.cTemplate = False
    #__init
#Script


@czcode.autoStr
class Classify:
    class Sorting:
        NONE, ALPHA, DATE = range(3)
    #Sorting

    def __init__(self):
        self.sorting = self.Sorting.NONE
        self.reverse = False
        self.images = False
        self.mute = False
    #__init
#Classify


@czcode.autoStr
class Rename:
    def __init__(self):
        self.extension = "mp4"
        self.target = ".avrename"
    #__init
#Classify


### aczutro ###################################################################
