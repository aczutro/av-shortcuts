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

"""command line parser"""


import argparse
from dataclasses import dataclass

class OptionID:
    """enum class for CommandLineParser.parseCommandLine"""
    DRY, AAC, MP3, NOA, COPYA, AB, AQ, CRF, C, S, T = range(11)

    @staticmethod
    def all():
        """returns list that contains all elements of the enum"""
        return range(11)
    #all
#OptionID


@dataclass
class GeneralOptions:
    """Bundles general options for CommandLineParser"""
    dry: bool = False
#GeneralOptions


@dataclass
class AudioOptions:
    """Bundles audio options for CommandLineParser"""
    command: list
#AudioOptions


@dataclass
class VideoOptions:
    """Bundles video options for CommandLineParser"""
    video: list
#VideoOptions


@dataclass
class TransformOptions:
    """Bundles transform options for CommandLineParser"""
    cropCommand: list
    scaleCommand: list
    timeCommand: list
#TransformOptions


class CommandLineParser:
    """command line parser"""

    def __init__(self, appDescription: str):
        """constructor

        :param appDescription:  app description for help text
        """
        self.appDescription = appDescription
        self.args = None
    #def

    def parseCommandLine(self, IDs: list) -> argparse.Namespace:
        """Parses command line and returns parsed arguments.

        :param IDs: list of OptionIDs to include
        """
        parser = argparse.ArgumentParser(description=self.appDescription,
                                         add_help=True)

        generalGroup = parser.add_argument_group(" general")
        audioGroup = parser.add_argument_group(" audio")
        videoGroup = parser.add_argument_group(" video")
        transGroup = parser.add_argument_group(" transforms")

        parser.add_argument("VIDEO_FILE",
                            type=str,
                            nargs="+",
                            help="video files to process"
                            )
        if OptionID.DRY in IDs:
            generalGroup.add_argument("-dry",
                                      action="store_true",
                                      help="only print FFmpeg command line; don't execute it"
                                      )
        #if
        if OptionID.AAC in IDs:
            audioGroup.add_argument("-aac",
                                    action="store_true",
                                    help="transcode audio to AAC (default)"
                                    )
        #if
        if OptionID.MP3 in IDs:
            audioGroup.add_argument("-mp3",
                                    action="store_true",
                                    help="transcode audio to MP3"
                                    )
        #if
        if OptionID.NOA in IDs:
            audioGroup.add_argument("-noa",
                                    action="store_true",
                                    help="produce no audio track "
                                    )
        #if
        if OptionID.COPYA in IDs:
            audioGroup.add_argument("-copya",
                                    action="store_true",
                                    help="copy audio track from input file"
                                    )
        #if
        if OptionID.AB in IDs:
            audioGroup.add_argument("-ab",
                                    dest="AUDIO_BITRATE",
                                    type=str,
                                    help="bitrate for output audio track. "
                                         "Defaults: if AAC, use FFmpeg's default; "
                                         "if MP3, use VBR with highest quality."
                                    )
        #if
        if OptionID.AQ in IDs:
            audioGroup.add_argument("-aq",
                                    dest="AUDIO_QUALITY",
                                    type=str,
                                    help="encode mp3 audio using VBR with this quality. "
                                         "Default: use VBR with highest quality."
                                    )
        #if
        if OptionID.CRF in IDs:
            videoGroup.add_argument("-crf",
                                    dest="CONSTANT_RATE_FACTOR",
                                    type=str,
                                    help="quality parameter for output video track. "
                                         "Default: FFmpeg's default (28 for h.265)."
                                    )
        #if
        if OptionID.C in IDs:
            transGroup.add_argument("-c",
                                    dest="CROP_FORMAT",
                                    type=str,
                                    help="CROP_LEFT[:CROP_RIGHT]:CROP_UP[:CROP_DOWN] "
                                         "If CROP_RIGHT *and* CROP_DOWN are left out, "
                                         "it is assumed that CROP_RIGHT = CROP_LEFT "
                                         "and CROP_DOWN = CROP_UP."
                                    )
        #if
        if OptionID.S in IDs:
            transGroup.add_argument("-s",
                                    dest="SCALE_FACTOR",
                                    type=float,
                                    help="apply scale video filter."
                                    )
        #if
        if OptionID.T in IDs:
            transGroup.add_argument("-t",
                                    dest="TIMESTAMPS",
                                    type=str,
                                    help="[START_TIME]:[END_TIME]  "
                                         "START_TIME and END_TIME are in seconds. "
                                         "If START_TIME is empty, START_TIME = 0. "
                                         "If END_TIME is empty, END_TIME = end of stream."
                                    )
        #if

        self.args = parser.parse_args()
    #parseCommandLine


    def getGeneralOptions(self) -> GeneralOptions:
        """Returns general options.

        Run parseCommandLine first!
        """
        ans = GeneralOptions()
        ans.dry = self.args.dry
        return ans
    #


    def getAudioOptions(self) -> AudioOptions:
        """Returns audio options.

        Run parseCommandLine first!
        """
        ans = AudioOptions()
        return ans
    #


    def getVideoOptions(self) -> VideoOptions:
        """Returns video options.

        Run parseCommandLine first!
        """
        ans = VideoOptions()
        return ans
    #


    def getTransformOptions(self) -> TransformOptions:
        """Returns transform options.

        Run parseCommandLine first!
        """
        ans = TransformOptions()
        return ans
    #

#CommandLineParser


# aczutro
