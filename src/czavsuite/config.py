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
    """enum class for config types
    """
    GENERAL, AUDIO, VIDEO, CROPPING, SCALING, CUTTING, PROBING = range(7)

# ConfigType


@czcode.autoStr
class General:
    def __init__(self):
        self.dry = False
    #__init
#General


@czcode.autoStr
class Audio:
    def __init__(self):
        self.noaudio = False
        self.codec = None
        self.bitrate = None
        self.quality = None
    #__init
#Audio


@czcode.autoStr
class Video:
    def __init__(self):
        self.crf = None
    #__init
#Video


@czcode.autoStr
class Cropping:
    def __init__(self):
        self.left = None
        self.right = None
        self.up = None
        self.down = None
    #__init
#Cropping


@czcode.autoStr
class Scaling:
    def __init__(self):
        self.factor = None
    #__init
#Scaling


@czcode.autoStr
class Cutting:
    def __init__(self):
        self.start = None
        self.end = None
    #__init
#Cutting


@czcode.autoStr
class Probing:
    FULL, VIDEO, AUDIO, DURATION = range(4)

    def __init__(self):
        self.mode = Probing.FULL
    #__init
#Cutting


### aczutro ###################################################################
