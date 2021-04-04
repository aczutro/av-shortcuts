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


from . import datastructs

import argparse


class OptionID:
    """enum class for option groups

    GENERAL:       include all general options
    AUDIO_CODEC:   include all audio codec options
    AUDIO_QUALITY: include all audio quality options
    VIDEO:         include all video options
    TRANS_CS:      include transform options -c and -s
    TRANS_T:       include transform option -t
    """
    GENERAL, \
    AUDIO_CODEC, \
    AUDIO_QUALITY, \
    VIDEO, \
    TRANS_CS, \
    TRANS_T \
        = range(6)

    @staticmethod
    def all():
        """returns list that contains all elements of the enum
        """
        return [ OptionID.GENERAL,
                 OptionID.AUDIO_CODEC,
                 OptionID.AUDIO_QUALITY,
                 OptionID.VIDEO,
                 OptionID.TRANS_CS,
                 OptionID.TRANS_T
                 ]
    #all

#OptionID


class CommandLineParser:
    """command line parser"""

    def __init__(self, appDescription: str, optionIDs: list, _info = None):
        """constructor

        :param appDescription:  app description for help text
        :param _INFO:           pointer to function for logging
        :param optionIDs:       list of OptionIDs to include
        """
        self.appDescription = appDescription
        self._info = _info
        self.optionIDs = optionIDs
    #__init__


    def parseCommandLine(self, infoFPointer = None) -> argparse.Namespace:
        """Parses command line and returns parsed arguments.

        """
        parser = argparse.ArgumentParser(description=self.appDescription,
                                         add_help=True)

        generalGroup = parser.add_argument_group(" general")
        audioGroup = parser.add_argument_group(" audio")
        videoGroup = parser.add_argument_group(" video")
        transGroup = parser.add_argument_group(" transforms")

        parser.add_argument("INPUT_FILE",
                            type=str,
                            nargs="+",
                            help="input files to process"
                            )
        if OptionID.GENERAL in self.optionIDs:
            generalGroup.add_argument("-dry",
                                      action="store_true",
                                      help="only print FFmpeg command line; don't execute it"
                                      )
        #if
        if OptionID.AUDIO_CODEC in self.optionIDs:
            audioGroup.add_argument("-aac",
                                    action="store_true",
                                    help="transcode audio to AAC (default)"
                                    )
            audioGroup.add_argument("-mp3",
                                    action="store_true",
                                    help="transcode audio to MP3"
                                    )
            audioGroup.add_argument("-noa",
                                    action="store_true",
                                    help="produce no audio track "
                                    )
            audioGroup.add_argument("-copya",
                                    action="store_true",
                                    help="copy audio track from input file"
                                    )
        #if
        if OptionID.AUDIO_QUALITY in self.optionIDs:
            audioGroup.add_argument("-ab",
                                    dest="AUDIO_BITRATE",
                                    type=str,
                                    help="bitrate for output audio track, e.g. '320k'. "
                                         "Default: use VBR."
                                    )
            audioGroup.add_argument("-aq",
                                    dest="AUDIO_QUALITY",
                                    type=int,
                                    help="encode mp3 audio using VBR with this quality. "
                                         "0 is best, 9 is worst. "
                                         "Default: 0"
                                    )
        #if
        if OptionID.VIDEO in self.optionIDs:
            videoGroup.add_argument("-crf",
                                    dest="CONSTANT_RATE_FACTOR",
                                    type=int,
                                    help="quality parameter for output video track. "
                                         "0 is best, 51 is worst. "
                                         "Default: FFmpeg's default (23 for h.264, 28 for h.265)."
                                    )
        #if
        if OptionID.TRANS_CS in self.optionIDs:
            transGroup.add_argument("-c",
                                    dest="CROP_FORMAT",
                                    type=str,
                                    help="CROP_LEFT[:CROP_RIGHT]:CROP_UP[:CROP_DOWN] "
                                         "If CROP_RIGHT *and* CROP_DOWN are left out, "
                                         "it is assumed that CROP_RIGHT = CROP_LEFT "
                                         "and CROP_DOWN = CROP_UP."
                                    )
            transGroup.add_argument("-s",
                                    dest="SCALE_FACTOR",
                                    type=float,
                                    help="apply scale video filter."
                                    )
        #if
        if OptionID.TRANS_T in self.optionIDs:
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

        if(self._info):
            self._info(self.args)
        #if

    #parseCommandLine


    def getPositionalArgs(self) -> list:
        """returns positional arguments
        """
        return self.args.INPUT_FILE
    #getPositionalArgs


    def getGeneralSettings(self) -> datastructs.GeneralSettings:
        """Returns general Settings.

        Run parseCommandLine first!
        """
        ans = datastructs.GeneralSettings(self.args.dry)
        return ans
    #getAudioSettings


    def getAudioSettings(self) -> datastructs.AudioSettings:
        """Returns audio Settings.

        Run parseCommandLine first!
        """
        ans = datastructs.AudioSettings()

        counter = 0
        if self.args.mp3:
            counter += 1
            ans.codec = 'libmp3lame'
        #if
        if self.args.aac:
            counter += 1
            ans.codec = 'aac'
        #if
        if self.args.copya:
            counter += 1
            ans.codec = 'copy'
        #if
        if self.args.noa:
            counter += 1
            ans.noaudio = True
        #if
        if counter > 1:
            raise Exception("only one of -aac, -mp3, -noa and -copya allowed")
        #if

        counter = 0
        if self.args.AUDIO_BITRATE is not None:
            counter += 1
            ans.bitrate = str(self.args.AUDIO_BITRATE)
        #if
        if self.args.AUDIO_QUALITY is not None:
            if self.args.AUDIO_QUALITY < 0 or self.args.AUDIO_QUALITY > 9:
                raise Exception("AUDIO_QUALITY must be between 0 and 9")
            #if
            counter += 1
            ans.quality = self.args.AUDIO_QUALITY
        #if
        if counter > 1:
            raise Exception("only one of -ab and -aq allowed")
        #if

        return ans
    #getAudioSettings


    def getVideoSettings(self) -> datastructs.VideoSettings:
        """Returns video Settings.

        Run parseCommandLine first!
        """
        ans = datastructs.VideoSettings()

        if self.args.CONSTANT_RATE_FACTOR is not None:
            if self.args.CONSTANT_RATE_FACTOR < 0 or self.args.CONSTANT_RATE_FACTOR > 51:
                raise Exception("CONSTANT_RATE_FACTOR must be between 0 and 51")
            #if
            ans.crf = str(self.args.CONSTANT_RATE_FACTOR)
        #if

        return ans
    #getVideoSettings


    def getTransformSettings(self) -> datastructs.TransformSettings:
        """Returns transform Settings.

        Run parseCommandLine first!
        """
        ans = datastructs.TransformSettings()
        return ans
    #getTransformSettings

#CommandLineParser


### aczutro ###################################################################
