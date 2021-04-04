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


from dataclasses import dataclass


@dataclass
class GeneralSettings:
    dry: bool = False
#GeneralSettings


@dataclass
class AudioCodecSettings:
    noaudio: bool = False
    codec: str = None
#AudioCodecSettings


@dataclass
class AudioQualitySettings:
    bitrate: str = None
    quality: str = None
#AudioQualitySettings


@dataclass
class VideoSettings:
    crf: str = None
#VideoSettings


@dataclass
class CropSettings:
    cropLeft: int = None
    cropRight: int = None
    cropUp: int = None
    cropDown: int = None
#CropSettings


@dataclass
class ScaleSettings:
    scaleFactor: float = None
#ScaleSettings


@dataclass
class TimeSettings:
    timeStart: float = None
    timeEnd: float = None
#TimeSettings


@dataclass
class Settings:
    general : GeneralSettings = None
    audioCodec : AudioCodecSettings = None
    audioQuality : AudioQualitySettings = None
    video : VideoSettings = None
    crop : CropSettings = None
    scale : ScaleSettings = None
    time : TimeSettings = None
#Settings


### aczutro ###################################################################
