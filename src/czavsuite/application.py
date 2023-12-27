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

from . import clp, config, probing, convert, scripts
from czutils.utils import czlogging, czsystem
import sys


_logger = czlogging.LoggingChannel(czsystem.appName(),
                                   czlogging.LoggingLevel.ERROR,
                                   colour=True)
clp.setLoggingOptions(czlogging.LoggingLevel.ERROR)
convert.setLoggingOptions(czlogging.LoggingLevel.ERROR)
probing.setLoggingOptions(czlogging.LoggingLevel.ERROR)


def _stderr(err: str):
    print("%s:" % czsystem.appName(), "error:", err)
#_stderr


class Application:
    """Base application class.
    Parses command line and calls _execute(), which needs to be implemented in
    derived classes.
    """
    def __init__(self, appDescription: str, configTypes: list, requireFiles=True):
        """
        :param requireFiles:    if True, expect input files (positional args)
        :param appDescription:  app description for command line help text
        :param configTypes:     command line options to parse
        """
        self.appDescription = appDescription
        self.configTypes = configTypes
        self.requireFiles = requireFiles

        self._parseCommandLine()

        try:
            self._execute()
        except convert.ConvertError as e:
            _stderr(e)
            sys.exit(1)
        except OSError as e:
            _stderr(e)
            sys.exit(1)
        #except
    #__init__


    def _parseCommandLine(self):
        try:
            CLP = clp.CommandLineParser(self.appDescription, self.configTypes, self.requireFiles)
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
        except czsystem.SystemCallError as e:
            _stderr(e)
        #except
    #_execute

#ApplicationProbe


class ApplicationConvert(Application):
    """entry point for av-convert
    """
    def __init__(self):
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


class ApplicationScript(Application):
    """entry point for av-script
    """
    def __init__(self):
        appDescription = "Creates a script to serialise convert jobs with individual job settings."
        configTypes = [ config.ConfigType.SCRIPT ]
        super().__init__(appDescription, configTypes)
    #__init__


    def _execute(self):
        try:
            scripts.avScript(self.inputFiles, self.config[config.ConfigType.SCRIPT])
        except KeyError as e:
            _logger.error("invalid config")
            raise e
        #except
    #_execute

#ApplicationScript


class ApplicationClassify(Application):
    """entry point for av-classify
    """
    def __init__(self):
        appDescription = ("Video and image classification helper.  In order to replace the default "
                          "media player command, set the environment variable AV_CLASS_PLAYER. "
                          "To replace the default image viewer, set AV_CLASS_VIEWER.")
        configTypes = [ config.ConfigType.CLASSIFY ]
        super().__init__(appDescription, configTypes)
    #__init__


    def _execute(self):
        try:
            scripts.avClassify(self.inputFiles, self.config[config.ConfigType.CLASSIFY])
        except KeyError as e:
            _logger.error("invalid config")
            raise e
        #except
    #_execute

#ApplicationClassify


class ApplicationRename(Application):
    """entry point for av-rename
    """
    def __init__(self):
        appDescription = ("Identifies pairs of files that have been converted using av-convert "
                          "(the 'before' and the 'after' file), moves them to a target directory "
                          "and renames them such that the before files are hidden (start with a "
                          "dot).")
        configTypes = [ config.ConfigType.RENAME ]
        super().__init__(appDescription, configTypes, requireFiles=False)
    #__init__


    def _execute(self):
        try:
            scripts.avRename(self.config[config.ConfigType.RENAME])
        except KeyError as e:
            _logger.error("invalid config")
            raise e
        #except
    #_execute

#ApplicationRename


### aczutro ###################################################################
