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
from czutils.utils import czlogging, czsystem
import argparse


_logger = czlogging.LoggingChannel("czavsuite.clp",
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
    _logger = czlogging.LoggingChannel("czavsuite.clp", level, colour=colour)
#setLoggingOptions


def _warning(*args):
    print("%s: warning:" % czsystem.appName(), " ".join(args))
#_warning


class CommandLineError(Exception):
    pass
#CommandLineError


class CommandLineParser:
    """Common command line parser.

    Constructor params:

    :param appDescription:  app description for help text
    :param configTypes:     list of OptionIDs to include
    """
    def __init__(self, appDescription: str, configTypes: list, requireFiles):
        self.args = []
        self.config = {}

        parser = argparse.ArgumentParser(description=appDescription,
                                         add_help=False)

        if requireFiles:
            parser.add_argument("FILE",
                                type=str,
                                nargs="+",
                                help="audio or video file"
                                )
        #if

        parser.add_argument("--help",
                            action="help",
                            help="show this help message and exit")
        parser.add_argument("--version",
                            action="version",
                            version=__version__,
                            help="show version number and exit")

        if config.ConfigType.GENERAL in configTypes:
            generalGroup = parser.add_argument_group()
            generalGroup.add_argument("-dry",
                                      action="store_true",
                                      help="only print FFmpeg command line; don't execute it"
                                      )
        #if
        if config.ConfigType.VIDEO in configTypes:
            videoGroup = parser.add_argument_group()
            videoGroup.add_argument("-avc",
                                    dest="vCodec",
                                    action="store_const",
                                    const="h264",
                                    default="h265",
                                    help="transcode video to AVC/H.264 (default: HEVC/H.265)"
                                    )
            videoGroup.add_argument("-vcopy",
                                    dest="vCodec",
                                    action="store_const",
                                    const="copy",
                                    default="h265",
                                    help="copy video track from input file"
                                    )
            videoGroup.add_argument("-vnull",
                                    dest="vCodec",
                                    action="store_const",
                                    const="null",
                                    default="h265",
                                    help="no video"
                                    )
            videoGroup.add_argument("-vq",
                                    metavar="CRF",
                                    dest="crf",
                                    type=int,
                                    help="video quality: 0 is best, 51 is worst (default: %s)" %
                                         config.Video().crf
                                    )
        #if
        if config.ConfigType.AUDIO in configTypes:
            audioGroup = parser.add_argument_group()
            audioGroup.add_argument("-mp3",
                                    dest="aCodec",
                                    action="store_const",
                                    const="mp3",
                                    default="aac",
                                    help="transcode audio to MP3 (default: AAC)"
                                    )
            audioGroup.add_argument("-acopy",
                                    dest="aCodec",
                                    action="store_const",
                                    const="copy",
                                    default="aac",
                                    help="copy audio track from input file"
                                    )
            audioGroup.add_argument("-anull",
                                    dest="aCodec",
                                    action="store_const",
                                    const="null",
                                    default="aac",
                                    help="no audio"
                                    )
            audioGroup.add_argument("-ab",
                                    metavar="BITRATE",
                                    dest="aBitrate",
                                    type=str,
                                    help="aac or mp3 bitrate (aac default: %s)" %
                                         config.Audio().bitrate
                                    )
            audioGroup.add_argument("-aq",
                                    metavar="QUALITY",
                                    dest="aQuality",
                                    type=int,
                                    help="mp3 only: 0 is best, 9 is worst (mp3 default: %s)" %
                                         config.Audio().quality
                                    )
        #if
        transGroup = parser.add_argument_group()
        if config.ConfigType.CROPPING in configTypes:
            transGroup.add_argument("-c",
                                    metavar="LEFT[:RIGHT]:UP[:DOWN]",
                                    dest="croppingFormat",
                                    type=str,
                                    help="number of pixels to crop away; "
                                         "if only LEFT:UP are given, "
                                         "RIGHT = LEFT and DOWN = UP"
                                    )
        #if
        if config.ConfigType.SCALING in configTypes:
            transGroup.add_argument("-s",
                                    metavar="FACTOR",
                                    dest="scalingFactor",
                                    type=float,
                                    help="scale video by this factor"
                                    )
        #if
        if config.ConfigType.CUTTING in configTypes:
            transGroup.add_argument("-t",
                                    dest="timestampRange",
                                    metavar="[START]:[END]",
                                    type=str,
                                    help="start and end times in seconds; "
                                         "empty START means START = 0; "
                                         "empty END means END = end of input stream"
                                    )
        #if
        if config.ConfigType.PROBING in configTypes:
            probeGroup = parser.add_argument_group()
            probeGroup.add_argument("-v",
                                    dest="probingMode",
                                    action="store_const",
                                    const=config.Probing.VIDEO,
                                    default=config.Probing.FULL,
                                    help="print only video information"
                                    )
            probeGroup.add_argument("-a",
                                    dest="probingMode",
                                    action="store_const",
                                    const=config.Probing.AUDIO,
                                    default=config.Probing.FULL,
                                    help="print only audio information"
                                    )
            probeGroup.add_argument("-d",
                                    dest="probingMode",
                                    action="store_const",
                                    const=config.Probing.DURATION,
                                    default=config.Probing.FULL,
                                    help="print only duration"
                                    )
            probeGroup.add_argument("-h",
                                    dest="headers",
                                    action="store_true",
                                    help="print table headers"
                                    )
        #if
        if config.ConfigType.SCRIPT in configTypes:
            scriptGroup = parser.add_argument_group()
            scriptGroup.add_argument("-dry",
                                     action="store_true",
                                     help="add -dry flag to av-convert commands in the script; "
                                          "this means that executing the script will only "
                                          "translate the script into FFmpeg commands that will be "
                                          "written into the 'betty' file"
                                     )
            scriptGroup.add_argument("-wilma",
                                     metavar="FILENAME",
                                     type=str,
                                     help="output file name (default: %s)" % config.Script().wilma
                                     )
            scriptGroup.add_argument("-betty",
                                     metavar="FILENAME",
                                     type=str,
                                     help="output file name for dry run (default: %s)" %
                                          config.Script().betty
                                     )
            scriptGroup.add_argument("-c",
                                     dest="cTemplate",
                                     action="store_true",
                                     help="add empty -c option to script"
                                     )
            scriptGroup.add_argument("-t",
                                     dest="tTemplate",
                                     action="store_true",
                                     help="add empty -t option to script"
                                     )
        #if
        if config.ConfigType.CLASSIFY in configTypes:
            scriptGroup = parser.add_argument_group()
            scriptGroup.add_argument("-i",
                                     action="store_true",
                                     help="use image viewer instead of media player"
                                     )
            scriptGroup.add_argument("-m",
                                     action="store_true",
                                     help="mute media player (ignored if AV_CLASS_PLAYER is set)"
                                     )
        #if
        if config.ConfigType.RENAME in configTypes:
            renameGroup = parser.add_argument_group()
            renameGroup.add_argument("-m4a",
                                     dest="extension",
                                     action="store_const",
                                     const="m4a",
                                     default="mp4",
                                     help="process m4a after files (default: mp4)"
                                     )
            renameGroup.add_argument("-mp3",
                                     dest="extension",
                                     action="store_const",
                                     const="mp3",
                                     default="mp4",
                                     help="process mp3 after files (default: mp4)"
                                     )
            renameGroup.add_argument("-target",
                                     metavar="DIRECTORY",
                                     type=str,
                                     help="move files to this directory (default: %s)" %
                                          config.Rename().target
                                     )
        #if

        try:
            container = parser.parse_args()
        except Exception as e:
            raise CommandLineError(e)
        #except

        if requireFiles:
            self.args = container.FILE
        #if
        self._cropAndScale = 0
        self._noOutput = 0

        for t in configTypes:
            if t == config.ConfigType.GENERAL:
                self._getGeneralSettings(container)
            elif t == config.ConfigType.VIDEO:
                self._getVideoSettings(container)
            elif t == config.ConfigType.AUDIO:
                self._getAudioSettings(container)
            elif t == config.ConfigType.CROPPING:
                self._getCroppingSettings(container)
            elif t == config.ConfigType.SCALING:
                self._getScalingSettings(container)
            elif t == config.ConfigType.CUTTING:
                self._getCuttingSettings(container)
            elif t == config.ConfigType.PROBING:
                self._getProbingSettings(container)
            elif t == config.ConfigType.SCRIPT:
                self._getScriptSettings(container)
            elif t == config.ConfigType.CLASSIFY:
                self._getClassifySettings(container)
            elif t == config.ConfigType.RENAME:
                self._getRenameSettings(container)
            else:
                _logger.error("invalid config type", t)
            #else
        #for

        if self._cropAndScale == 3:
            raise CommandLineError("-c and -s cannot be used at the same time")
        #if
        if self._noOutput == 3:
            raise CommandLineError("cowardly refusing to create media files with no video and no "
                                   "audio")
        #if
    #__init__


    def _getGeneralSettings(self, container):
        conf = config.General()
        conf.dry = container.dry
        self.config[config.ConfigType.GENERAL] = conf
    #_getGeneralSettings


    def _getVideoSettings(self, container):
        conf = config.Video()
        conf.codec = container.vCodec

        if conf.codec == "null":
            self._noOutput |= 1
        #if

        if container.crf is not None:
            if conf.codec == "copy":
                _warning("copying input video without transcoding; ignoring -vq")
            elif conf.codec == "null":
                _warning("no video output; ignoring -vq")
            elif container.crf < 0 or container.crf > 51:
                raise CommandLineError("CRF must be between 0 and 51")
            #if
            conf.crf = str(container.crf)
        #if

        self.config[config.ConfigType.VIDEO] = conf
    #_getVideoSettings


    def _getAudioSettings(self, container):
        conf = config.Audio()
        conf.codec = container.aCodec

        if conf.codec == "aac":
            if container.aBitrate is not None:
                conf.bitrate = container.aBitrate
            #if
            if container.aQuality is not None:
                _warning("using AAC audio; ignoring -aq")
            #if
        elif conf.codec == "mp3":
            conf.bitrate = None
            if container.aQuality is not None and container.aBitrate is not None:
                raise CommandLineError("-ab and -aq cannot be used together")
            elif container.aBitrate is not None:
                conf.bitrate = container.aBitrate
                conf.quality = None
            elif container.aQuality is not None:
                if container.aQuality < 0 or container.aQuality > 9:
                    raise CommandLineError("QUALITY must be between 0 and 9")
                else:
                    conf.quality = str(container.aQuality)
                #else
            #elif
        elif conf.codec == "copy":
            if container.aQuality is not None:
                _warning("copying input audio without transcoding; ignoring -aq")
            #if
            if container.aBitrate is not None:
                _warning("copying input audio without transcoding; ignoring -ab")
            #if
        elif conf.codec == "null":
            self._noOutput |= 2
            if container.aQuality is not None:
                _warning("no audio output; ignoring -aq")
            #if
            if container.aBitrate is not None:
                _warning("no audio output; ignoring -ab")
            #if
        else:
            _logger.error("invalid conf.codec value")
            raise Exception("invalid conf.codec value")
        #else

        self.config[config.ConfigType.AUDIO] = conf
    #_getAudioSettings


    def _getCroppingSettings(self, container):
        conf = config.Cropping()
        conf.valid = False

        if container.croppingFormat is not None:
            conf.valid = True
            self._cropAndScale |= 1

            tokens = container.croppingFormat.split(":")
            try:
                if len(tokens) == 2:
                    conf.left = int(tokens[0])
                    conf.right = int(tokens[0])
                    conf.up = int(tokens[1])
                    conf.down = int(tokens[1])
                elif len(tokens) == 4:
                    conf.left = int(tokens[0])
                    conf.right = int(tokens[1])
                    conf.up = int(tokens[2])
                    conf.down = int(tokens[3])
                else:
                    raise CommandLineError("cropping format: bad number of tokens")
                #else
            except ValueError as e:
                raise CommandLineError("-c: %s" % e)
            #except

            if conf.left < 0 or conf.right < 0 or conf.up < 0 or conf.down < 0:
                raise CommandLineError("cropping format: a negative number "
                                       "of pixels doesn't make sense")
            #if
        #if

        self.config[config.ConfigType.CROPPING] = conf
    #_getCroppingSettings


    def _getScalingSettings(self, container):
        conf = config.Scaling()
        conf.valid = False

        if container.scalingFactor is not None:
            conf.valid = True
            self._cropAndScale |= 2

            if container.scalingFactor == 0:
                raise CommandLineError("what do you expect to get if you scale video by factor 0?")
            elif container.scalingFactor < 0:
                raise CommandLineError("cowardly refusing to scale video by a negative factor")
            else:
                conf.factor = container.scalingFactor
            #else
        #if

        self.config[config.ConfigType.SCALING] = conf
    #_getScalingSettings


    def _getCuttingSettings(self, container):
        conf = config.Cutting()
        conf.valid = False
        conf.start = None
        conf.end = None

        negative = False
        inconsistent = False

        if container.timestampRange is not None:
            conf.valid = True

            tokens = container.timestampRange.split(":")
            try:
                if len(tokens) == 2:
                    if len(tokens[0]) + len(tokens[1]) == 0:
                        raise CommandLineError("cutting timestamps: both tokens cannot be empty "
                                               "at the same time")
                    elif len(tokens[0]) == 0:
                        conf.end = float(tokens[1])
                        if conf.end < 0:
                            negative = True
                        #if
                    elif len(tokens[1]) == 0:
                        conf.start = float(tokens[0])
                        if conf.start < 0:
                            negative = True
                        #if
                    else:
                        conf.start = float(tokens[0])
                        conf.end = float(tokens[1])
                        if conf.start < 0 or conf.end < 0:
                            negative = True
                        #if
                        if not conf.start < conf.end:
                            inconsistent = True
                        #if
                    #else
                else:
                    raise CommandLineError("cutting timestamps: bad number of tokens")
                #else
            except ValueError as e:
                raise CommandLineError("-t: %s" % e)
            #except

            if negative:
                raise CommandLineError("cutting timestamps: start and end times cannot be negative")
            #if
            if inconsistent:
                raise CommandLineError("cutting timestamps: start time must be less than end time")
            #if
        #if

        self.config[config.ConfigType.CUTTING] = conf
    #_getCuttingSettings


    def _getProbingSettings(self, container):
        conf = config.Probing()
        conf.headers = container.headers
        conf.mode = container.probingMode
        self.config[config.ConfigType.PROBING] = conf
    #_getProbingSettings


    def _getScriptSettings(self, container):
        conf = config.Script()
        conf.dry = container.dry
        conf.cTemplate = container.cTemplate
        conf.tTemplate = container.tTemplate

        if container.wilma is not None:
            conf.wilma = container.wilma
        #if
        if container.betty is not None:
            conf.betty = container.betty
            if not conf.dry:
                _warning("producing a non-dry script; ignoring -betty")
            #if
        #if

        self.config[config.ConfigType.SCRIPT] = conf
    #_getScriptSettings


    def _getClassifySettings(self, container):
        conf = config.Classify()
        conf.images = container.i
        conf.mute = container.m
        if conf.images and conf.mute:
            _warning("using photo viewer; ignoring -m")
        #if
        self.config[config.ConfigType.CLASSIFY] = conf
    #_getClassifySettings


    def _getRenameSettings(self, container):
        conf = config.Rename()
        conf.extension = container.extension
        if container.target is not None:
            conf.target = container.target
        #if
        self.config[config.ConfigType.RENAME] = conf
    #_getRenameSettings

#CommandLineParser


### aczutro ###################################################################
