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

"""command line parser"""

from . import config, __version__
from czutils.utils import czlogging
import argparse


_logger = czlogging.LoggingChannel("czavsuite.clp",
                                   czlogging.LoggingLevel.ERROR,
                                   colour=True)


class CommandLineError(Exception):
    pass


class CommandLineParser:
    """common command line parser"""

    def __init__(self, appDescription: str, configTypes: list):
        """constructor

        :param appDescription:  app description for help text
        :param configTypes:     list of OptionIDs to include
        """
        self.appDescription = appDescription
        self.configTypes = configTypes
        self.args = []
        self.config = []

    # __init__


    def parseCommandLine(self):
        """parses command line and stores the settings internally

        """
        parser = argparse.ArgumentParser(description=self.appDescription,
                                         add_help=False)

        generalGroup = parser.add_argument_group(" general")
        audioGroup = parser.add_argument_group(" audio")
        videoGroup = parser.add_argument_group(" video")
        transGroup = parser.add_argument_group(" transforms")

        parser.add_argument("FILE",
                            type=str,
                            nargs="+",
                            help="audio or video file"
                            )
        parser.add_argument("--help",
                            action="help",
                            help="show this help message and exit")
        parser.add_argument("--version",
                            action="version",
                            version=__version__,
                            help="show version number and exit")
        if config.ConfigType.GENERAL in self.configTypes:
            generalGroup.add_argument("-dry",
                                      action="store_true",
                                      help="only print FFmpeg command line; don't execute it"
                                      )
        # if
        if config.ConfigType.AUDIO in self.configTypes:
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
        # if
        if config.ConfigType.VIDEO in self.configTypes:
            videoGroup.add_argument("-crf",
                                    dest="CONSTANT_RATE_FACTOR",
                                    type=int,
                                    help="quality parameter for output video track. "
                                         "0 is best, 51 is worst. "
                                         "Default: FFmpeg's default (23 for h.264, 28 for h.265)."
                                    )
        # if
        if config.ConfigType.CROPPING in self.configTypes:
            transGroup.add_argument("-c",
                                    dest="CROP_FORMAT",
                                    type=str,
                                    help="CROP_LEFT[:CROP_RIGHT]:CROP_UP[:CROP_DOWN] "
                                         "If CROP_RIGHT *and* CROP_DOWN are left out, "
                                         "it is assumed that CROP_RIGHT = CROP_LEFT "
                                         "and CROP_DOWN = CROP_UP."
                                    )
        # if
        if config.ConfigType.SCALING in self.configTypes:
            transGroup.add_argument("-s",
                                    dest="SCALE_FACTOR",
                                    type=float,
                                    help="apply scale video filter."
                                    )
        # if
        if config.ConfigType.CUTTING in self.configTypes:
            transGroup.add_argument("-t",
                                    dest="TIMESTAMPS",
                                    type=str,
                                    help="[START_TIME]:[END_TIME]  "
                                         "START_TIME and END_TIME are in seconds. "
                                         "If START_TIME is empty, START_TIME = 0. "
                                         "If END_TIME is empty, END_TIME = end of stream."
                                    )
        # if
        if config.ConfigType.PROBING in self.configTypes:
            parser.add_argument("-v",
                                dest="probingMode",
                                action="store_const",
                                const=config.Probing.VIDEO,
                                default=config.Probing.FULL,
                                help="print only video information"
                                )
            parser.add_argument("-a",
                                dest="probingMode",
                                action="store_const",
                                const=config.Probing.AUDIO,
                                default=config.Probing.FULL,
                                help="print only audio information"
                                )
            parser.add_argument("-d",
                                dest="probingMode",
                                action="store_const",
                                const=config.Probing.DURATION,
                                default=config.Probing.FULL,
                                help="print only duration"
                                )
            parser.add_argument("-h",
                                dest="headers",
                                action="store_const",
                                const=True,
                                default=False,
                                help="print table headers"
                                )
        # if

        try:
            container = parser.parse_args()
        except Exception as e:
            raise CommandLineError(e)
        #except

        self.args = container.FILE

        for t in self.configTypes:
            if t == config.ConfigType.GENERAL:
                self._getGeneralSettings(container)
            elif t == config.ConfigType.AUDIO:
                self._getAudioSettings(container)
            elif t == config.ConfigType.VIDEO:
                self._getVideoSettings(container)
            elif t == config.ConfigType.CROPPING:
                self._getCroppingSettings(container)
            elif t == config.ConfigType.SCALING:
                self._getScalingSettings(container)
            elif t == config.ConfigType.CUTTING:
                self._getCuttingSettings(container)
            elif t == config.ConfigType.PROBING:
                self._getProbingSettings(container)
            else:
                _logger.error("invalid config type", t)
            #else
        #for

    # parseCommandLine


    def _getGeneralSettings(self, container):
        conf = config.General()
        conf.dry = container.dry
        self.config.append(conf)

    # _getGeneralSettings


    def _getAudioSettings(self, container):
        conf = config.Audio()

        counter = 0
        if container.mp3:
            counter += 1
            conf.codec = 'libmp3lame'
        # if
        if container.aac:
            counter += 1
            conf.codec = 'aac'
        # if
        if container.copya:
            counter += 1
            conf.codec = 'copy'
        # if
        if container.noa:
            counter += 1
            conf.noaudio = True
        # if
        if counter > 1:
            raise CommandLineError("only one of -aac, -mp3, -noa and -copya allowed")
        # if

        counter = 0
        if container.AUDIO_BITRATE is not None:
            counter += 1
            conf.bitrate = str(container.AUDIO_BITRATE)
        # if
        if container.AUDIO_QUALITY is not None:
            if container.AUDIO_QUALITY < 0 or container.AUDIO_QUALITY > 9:
                raise CommandLineError("AUDIO_QUALITY must be between 0 and 9")
            # if
            counter += 1
            conf.quality = container.AUDIO_QUALITY
        # if
        if counter > 1:
            raise CommandLineError("only one of -ab and -aq allowed")
        # if

        self.config.append(conf)

    # _getAudioSettings


    def _getVideoSettings(self, container):
        conf = config.Video()
        if container.CONSTANT_RATE_FACTOR is not None:
            if container.CONSTANT_RATE_FACTOR < 0 or container.CONSTANT_RATE_FACTOR > 51:
                raise CommandLineError("CONSTANT_RATE_FACTOR must be between 0 and 51")
            # if
            conf.crf = str(container.CONSTANT_RATE_FACTOR)
        # if
        self.config.append(conf)

    # _getVideoSettings


    def _getCroppingSettings(self, container):
        conf = config.Cropping()
        if container.CROP_FORMAT is not None:
            tokens = container.CROP_FORMAT.split(":")
            try:
                if len(tokens) == 2:
                    conf.left = int(tokens[0])
                    conf.right = int(tokens[0])
                    conf.up = int(tokens[1])
                    conf.down = int(tokens[1])
                elif len(tokens) == 4:
                    conf.crop = (int(t) for t in tokens)
                else:
                    raise CommandLineError("bad number of tokens: CROP_FORMAT")
                #else
            except ValueError as v:
                raise Exception(v)
            #except
            if not min(( t >= 0 for t in conf.crop)):
                raise CommandLineError("bad CROP_FORMAT: negative value")
            #if
        # if
        self.config.append(conf)

    # _getCroppingSettings


    def _getScalingSettings(self, container):
        raise Exception("IMPLEMENT ME!")

    # _getScalingSettings


    def _getCuttingSettings(self, container):
        raise Exception("IMPLEMENT ME!")
    # _getCuttingSettings


    def _getProbingSettings(self, container):
        conf = config.Probing()
        conf.headers = container.headers
        conf.mode = container.probingMode
        self.config.append(conf)
    # _getProbingSettings

# CommandLineParser


### aczutro ###################################################################
