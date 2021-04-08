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


from . import settings

import argparse


class OptionID:
    """enum class for option groups
    """
    GENERAL, \
    AUDIO_CODEC, \
    AUDIO_QUALITY, \
    VIDEO, \
    TRANS_C, \
    TRANS_S, \
    TRANS_T \
        = range(7)

    @staticmethod
    def all():
        """returns list that contains all elements of the enum
        """
        return range(7)
    #all

#OptionID


class CommandLineParser:
    """command line parser"""

    def __init__(self, appDescription: str, optionIDs: list, fInfo = None):
        """constructor

        :param appDescription:  app description for help text
        :param _info:           pointer to function for logging
        :param optionIDs:       list of OptionIDs to include
        """
        self.appDescription = appDescription
        self.fInfo = fInfo
        self.optionIDs = optionIDs
        self.args = []
        self.settings = settings.Settings()
    #__init__


    def parseCommandLine(self):
        """parses command line and stores the settings internally

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
        if OptionID.TRANS_C in self.optionIDs:
            transGroup.add_argument("-c",
                                    dest="CROP_FORMAT",
                                    type=str,
                                    help="CROP_LEFT[:CROP_RIGHT]:CROP_UP[:CROP_DOWN] "
                                         "If CROP_RIGHT *and* CROP_DOWN are left out, "
                                         "it is assumed that CROP_RIGHT = CROP_LEFT "
                                         "and CROP_DOWN = CROP_UP."
                                    )
        #if
        if OptionID.TRANS_S in self.optionIDs:
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

        container = parser.parse_args()

        if(self.fInfo):
            self.fInfo(container)
        #if

        self.args = container.INPUT_FILE

        if OptionID.GENERAL in self.optionIDs:
            self._deriveGeneralSettings(container)
        else:
            self.settings.general = None
        #else
        if OptionID.AUDIO_CODEC in self.optionIDs:
            self._deriveAudioCodecSettings(container)
        else:
            self.settings.audioCodec = None
        #else
        if OptionID.AUDIO_QUALITY in self.optionIDs:
            self._deriveAudioQualitySettings(container)
        else:
            self.settings.audioQuality = None
        #else
        if OptionID.VIDEO in self.optionIDs:
            self._deriveVideoSettings(container)
        else:
            self.settings.video = None
        #else
        if OptionID.TRANS_C in self.optionIDs:
            self._deriveCropSettings(container)
        else:
            self.settings.crop = None
        #else
        if OptionID.TRANS_S in self.optionIDs:
            self._deriveScaleSettings(container)
        else:
            self.settings.scale = None
        #else
        if OptionID.TRANS_T in self.optionIDs:
            self._deriveTimeSettings(container)
        else:
            self.settings.time = None
        #else
    #parseCommandLine


    def _deriveGeneralSettings(self, container):
        self.settings.general.dry = container.dry
    #_deriveGeneralSettings


    def _deriveAudioCodecSettings(self, container):
        counter = 0
        if container.mp3:
            counter += 1
            self.settings.audioCodec.codec = 'libmp3lame'
        #if
        if container.aac:
            counter += 1
            self.settings.audioCodec.codec = 'aac'
        #if
        if container.copya:
            counter += 1
            self.settings.audioCodec.codec = 'copy'
        #if
        if container.noa:
            counter += 1
            self.settings.audioCodec.noaudio = True
        #if
        if counter > 1:
            raise Exception("only one of -aac, -mp3, -noa and -copya allowed")
        #if
    #_deriveAudioCodecSettings


    def _deriveAudioQualitySettings(self, container):
        counter = 0
        if container.AUDIO_BITRATE is not None:
            counter += 1
            self.settings.audioQuality.bitrate = str(container.AUDIO_BITRATE)
        #if
        if container.AUDIO_QUALITY is not None:
            if container.AUDIO_QUALITY < 0 or container.AUDIO_QUALITY > 9:
                raise Exception("AUDIO_QUALITY must be between 0 and 9")
            #if
            counter += 1
            self.settings.audioQuality.quality = container.AUDIO_QUALITY
        #if
        if counter > 1:
            raise Exception("only one of -ab and -aq allowed")
        #if
    #__deriveAudioQualitySettings


    def _deriveVideoSettings(self, container):
        if container.CONSTANT_RATE_FACTOR is not None:
            if container.CONSTANT_RATE_FACTOR < 0 or container.CONSTANT_RATE_FACTOR > 51:
                raise Exception("CONSTANT_RATE_FACTOR must be between 0 and 51")
            #if
            self.settings.video.crf = str(container.CONSTANT_RATE_FACTOR)
        #if
    #_deriveVideoSettings


    def _deriveCropSettings(self, container):
        pass
        #raise Exception("IMPLEMENT ME!")
    #_deriveCropSettings


    def _deriveScaleSettings(self, container):
        pass
        #raise Exception("IMPLEMENT ME!")
    #_deriveScaleSettings


    def _deriveTimeSettings(self, container):
        pass
        #raise Exception("IMPLEMENT ME!")
    #_deriveTimeSettings

#CommandLineParser


### aczutro ###################################################################
