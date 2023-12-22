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

"""main application classes"""

from . import clp, config, probing, ffmpeg
from czutils.utils import czlogging, czsystem
import sys


_logger = czlogging.LoggingChannel(czsystem.appName(),
                                   czlogging.LoggingLevel.ERROR,
                                   colour=True)


def _stderr(err: str):
    print("%s:" % czsystem.appName(), "error:", err)
#_stderr


class Application:
    """base application class

    provides interface for command line parsing and task execution
    """

    def __init__(self, appDescription: str, configTypes: list):
        """constructor

        :param appDescription:  app description for help text
        :param configTypes:     options to include in command line
        """
        self.appDescription = appDescription
        self.configTypes = configTypes
    #__init__


    def execute(self):
        """executes all tasks
        """
        self._parseCommandLine()
        try:
            self._execute()
        except ffmpeg.SubprocessError as e:
            _stderr(e)
        #except
    #execute


    def _parseCommandLine(self):
        CLP = clp.CommandLineParser(self.appDescription, self.configTypes)
        try:
            CLP.parseCommandLine()
        except clp.CommandLineError as e:
            _logger.error(e)
            _stderr(e)
            sys.exit(2)
        #except

        self.inputFiles = CLP.args
        self.config = CLP.config

        _logger.info("files:", self.inputFiles)
        _logger.info("config:", [ str(c) for c in self.config ])
    #_parseCommandLine


    def _execute(self):
        raise Exception("%s._execute: IMPLEMENT ME!" % type(self).__name__)
    #_execute

#Application


class ApplicationProbe(Application):
    """main application class for av-probe
    """
    def __init__(self):
        """constructor
        """
        appDescription = "ffprobe wrapper"
        configTypes = [ config.ConfigType.PROBING ]
        super().__init__(appDescription, configTypes)
    #__init__

    def _execute(self):
        for conf in self.config:
            if type(conf) is config.Probing:
                probing.avProbe(self.inputFiles, conf)
                break
            #if
        else:
            raise Exception("invalid configuration")
        #else
    #_execute

#ApplicationCut


class ApplicationCut(Application):
    """main application class for av-to-mp4
    """
    def __init__(self):
        """constructor
        """
        appDescription = "cuts out video between two timestamps (no transcoding)"
        configTypes = [ config.ConfigType.GENERAL, config.ConfigType.CUTTING ]
        super().__init__(appDescription, configTypes)
    #__init__

#ApplicationCut


class ApplicationPlay(Application):
    """main application class for av-to-mp4
    """
    def __init__(self):
        """constructor
        """
        appDescription = "plays video and offers a simplified way of specifying "\
                         "cropping and scaling parameters"
        configTypes = [ config.ConfigType.GENERAL,
                        config.ConfigType.CROPPING,
                        config.ConfigType.SCALING,
                        config.ConfigType.CUTTING ]
        super().__init__(appDescription, configTypes)
    #__init__

#ApplicationPlay


class ApplicationToAAC(Application):
    """main application class for av-to-mp4
    """
    def __init__(self):
        """constructor
        """
        appDescription = "extracts AAC audio from video files"
        configTypes = [ config.ConfigType.GENERAL ]
        super().__init__(appDescription, configTypes)
    #__init__

#ApplicationToAAC


class ApplicationToMp3(Application):
    """main application class for av-to-mp4
    """
    def __init__(self):
        """constructor
        """
        appDescription = "extracts audio track from audio or video file "\
                         "and converts it to mp3"
        configTypes = [ config.ConfigType.GENERAL, config.ConfigType.AUDIO ]
        super().__init__(appDescription, configTypes)
    #__init__

#ApplicationToMp3


class ApplicationToMp4(Application):
    """main application class for av-to-mp4
    """
    def __init__(self):
        """constructor
        """
        appDescription = "converts video to mp4 (h.265 + aac) using "\
                         "a set of sensible defaults"
        configTypes = []
        super().__init__(appDescription, configTypes)
    #__init__

#ApplicationToMp4


### aczutro ###################################################################
