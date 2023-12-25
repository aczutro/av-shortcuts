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

from . import clp, config, probing, convert, utils
from czutils.utils import czlogging, czsystem
import sys


_logger = czlogging.LoggingChannel(czsystem.appName(),
                                   czlogging.LoggingLevel.ERROR,
                                   colour=True)
clp.setLoggingOptions(czlogging.LoggingLevel.ERROR)
convert.setLoggingOptions(czlogging.LoggingLevel.ERROR)
probing.setLoggingOptions(czlogging.LoggingLevel.ERROR)
utils.setLoggingOptions(czlogging.LoggingLevel.ERROR)


def _stderr(err: str):
    print("%s:" % czsystem.appName(), "error:", err)
#_stderr


class Application:
    """Base application class.
    Parses command line and calls _execute(), which needs to be implemented in
    derived classes.
    """
    def __init__(self, appDescription: str, configTypes: list):
        """constructor

        :param appDescription:  app description for help text
        :param configTypes:     options to include in command line
        """
        self.appDescription = appDescription
        self.configTypes = configTypes

        self._parseCommandLine()

        try:
            self._execute()
        except convert.ConvertError as e:
            _stderr(e)
        #except
    #__init__


    def _parseCommandLine(self):
        try:
            CLP = clp.CommandLineParser(self.appDescription, self.configTypes)
            self.inputFiles = CLP.args
            self.config = CLP.config
        except clp.CommandLineError as e:
            _stderr(e)
            sys.exit(2)
        #except

        _logger.info("files:", self.inputFiles)
        _logger.info("config:", "\n".join([ str(self.config[key]) for key in self.config ]))
    #_parseCommandLine


    def _execute(self):
        raise Exception("%s._execute: IMPLEMENT ME!" % type(self).__name__)
    #_execute

#Application


class ApplicationProbe(Application):
    """entry point for av-probe
    """
    def __init__(self):
        """constructor
        """
        appDescription = "Extracts audio and video information from media files."
        configTypes = [ config.ConfigType.PROBING ]
        super().__init__(appDescription, configTypes)
    #__init__


    def _execute(self):
        try:
            probing.avProbe(self.inputFiles,
                            self.config[config.ConfigType.PROBING].mode,
                            self.config[config.ConfigType.PROBING].headers)
        except KeyError as e:
            _logger.error("invalid config")
            raise e
        #except
    #_execute

#ApplicationProbe


class ApplicationConvert(Application):
    """entry point for av-convert
    """
    def __init__(self):
        """constructor
        """
        appDescription = "Converts media files to mp4, m4a or mp3."
        configTypes = [ config.ConfigType.GENERAL,
                        config.ConfigType.VIDEO,
                        config.ConfigType.AUDIO,
                        config.ConfigType.CROPPING,
                        config.ConfigType.SCALING,
                        config.ConfigType.CUTTING ]
        super().__init__(appDescription, configTypes)
    #__init__


    def _execute(self):
        try:
            convert.avConvert(self.inputFiles,
                              self.config[config.ConfigType.GENERAL],
                              self.config[config.ConfigType.VIDEO],
                              self.config[config.ConfigType.AUDIO],
                              self.config[config.ConfigType.CROPPING],
                              self.config[config.ConfigType.SCALING],
                              self.config[config.ConfigType.CUTTING])
        except KeyError as e:
            _logger.error("invalid config")
            raise e
        #except
    #_execute

#ApplicationConvert


class ApplicationPlay(Application):
    """entry point for av-play
    """
    def __init__(self):
        """constructor
        """
        appDescription = "Plays video and offers a simplified way of specifying "\
                         "cropping and scaling parameters."
        configTypes = [ config.ConfigType.CROPPING,
                        config.ConfigType.SCALING,
                        config.ConfigType.CUTTING ]
        super().__init__(appDescription, configTypes)
    #__init__


    def _execute(self):
        try:
            convert.avPlay(self.inputFiles,
                           self.config[config.ConfigType.CROPPING],
                           self.config[config.ConfigType.SCALING],
                           self.config[config.ConfigType.CUTTING])
        except KeyError as e:
            _logger.error("invalid config")
            raise e
        #except
    #_execute

#ApplicationPlay


### aczutro ###################################################################
