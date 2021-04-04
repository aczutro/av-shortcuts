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

"""main application classes"""

from . import czlogging
from . import clp

import os.path
import sys


class Application:
    """base application class

    provides interface for command line parsing and task execution
    """

    def __init__(self, appDescription: str, optionsIDs: list):
        """constructor

        :param appDescription:  app description for help text
        :param optionsIDs:      options to include in command line
        """
        self.appName = os.path.basename(sys.argv[0])
        self.appDescription = appDescription
        self.optionIDs = optionsIDs
        self._info, self._warning, self._error = czlogging.initLogging("INFO")
    #__init__


    def parseCommandLine(self):
        """parses command line"""

        CLP = clp.CommandLineParser(self.appDescription, self.optionIDs,
                                    _info=self._info)
        CLP.parseCommandLine()

        try:
            self.inputFiles = CLP.getPositionalArgs()
            self.general = CLP.getGeneralSettings()
            self.audio = CLP.getAudioSettings()
            self.video = CLP.getVideoSettings()
            self.transforms = CLP.getTransformSettings()
        except Exception as e:
            self._error(e)
        #except

    #parseCommandLine


    def execute(self):
        """executes all tasks
        """
        self._error("execute: IMPLEMENT ME!")
    #execute

#Application


class ApplicationCut(Application):
    """main application class for av-to-mp4

    provides interface for command line parsing and task execution
    """
    def __init__(self):
        """constructor
        """
        appDescription = "cuts out video between two timestamps (no transcoding)"
        optionIDs = [ clp.OptionID.GENERAL, clp.OptionID.TRANS_T ]
        super().__init__(appDescription, optionIDs)
    #__init__

#ApplicationCut


class ApplicationPlay(Application):
    """main application class for av-to-mp4

    provides interface for command line parsing and task execution
    """
    def __init__(self):
        """constructor
        """
        appDescription = "plays video and offers a simplified way of specifying "\
                         "cropping and scaling parameters"
        optionIDs = [ clp.OptionID.GENERAL,
                      clp.OptionID.TRANS_CS, clp.OptionID.TRANS_T ]
        super().__init__(appDescription, optionIDs)
    #__init__

#ApplicationPlay


class ApplicationToAAC(Application):
    """main application class for av-to-mp4

    provides interface for command line parsing and task execution
    """
    def __init__(self):
        """constructor
        """
        appDescription = "extracts AAC audio from video files"
        optionIDs = [ clp.OptionID.GENERAL ]
        super().__init__(appDescription, optionIDs)
    #__init__

#ApplicationToAAC


class ApplicationToMp3(Application):
    """main application class for av-to-mp4

    provides interface for command line parsing and task execution
    """
    def __init__(self):
        """constructor
        """
        appDescription = "extracts audio track from audio or video file "\
                         "and converts it to mp3"
        optionIDs = [ clp.OptionID.GENERAL, clp.OptionID.AUDIO_QUALITY ]
        super().__init__(appDescription, optionIDs)
    #__init__

#ApplicationToMp3


class ApplicationToMp4(Application):
    """main application class for av-to-mp4

    provides interface for command line parsing and task execution
    """
    def __init__(self):
        """constructor
        """
        appDescription = "converts video to mp4 (h.265) using "\
                         "a set of sensible defaults"
        optionIDs = clp.OptionID.all()
        super().__init__(appDescription, optionIDs)
    #__init__


    def execute(self):
        """executes all tasks
        """
        self._info(self.inputFiles)
        self._info(self.general)
        self._info(self.audio)
        self._info(self.video)
        self._info(self.transforms)

    #execute

#ApplicationToMp4


### aczutro ###################################################################
