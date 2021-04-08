# av-shortcuts - FFmpeg wrapper with a simplified command line
#
# Copyright 2020 - 2021 Alexander Czutro, github@czutro.ch
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

from .czutils import autoStr


@autoStr
class GeneralSettings:
    def __init__(self):
        self.dry = False
    #__init
#GeneralSettings


@autoStr
class AudioCodecSettings:
    def __init__(self):
        self.noaudio = False
        self.codec = None
    #__init
#AudioCodecSettings


@autoStr
class AudioQualitySettings:
    def __init__(self):
        self.bitrate = None
        self.quality = None
    #__init
#AudioQualitySettings


@autoStr
class VideoSettings:
    def __init__(self):
        self.crf = None
    #__init
#VideoSettings


@autoStr
class CropSettings:
    def __init__(self):
        self.cropLeft = None
        self.cropRight = None
        self.cropUp = None
        self.cropDown = None
    #__init
#CropSettings


@autoStr
class ScaleSettings:
    def __init__(self):
        self.scaleFactor = None
    #__init
#ScaleSettings


@autoStr
class TimeSettings:
    def __init__(self):
        self.timeStart = None
        self.timeEnd = None
    #__init
#TimeSettings


@autoStr
class Settings:
    def __init__(self):
        self.general = GeneralSettings()
        self.audioCodec = AudioCodecSettings()
        self.audioQuality = AudioQualitySettings()
        self.video = VideoSettings()
        self.crop = CropSettings()
        self.scale = ScaleSettings()
        self.time = TimeSettings()
    #__init__
#Settings


### aczutro ###################################################################
