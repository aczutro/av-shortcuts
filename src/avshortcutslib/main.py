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

"""main routines"""

from . import clp
from . import czlogging
from . import execution


def _main(executor, optionIDs: list, appDescription: str):
    """generic main routine

    :param executor:        the executor
    :param optionIDs:       option IDs to include in command line parser
    :param appDescription:  app description for help text
    """
    _INFO, _WARNING, _ERROR = czlogging.initLogging("INFO")

    CLP = clp.CommandLineParser(appDescription, _INFO=_INFO)
    CLP.parseCommandLine(optionIDs)

    try:
        inputFiles = CLP.getPositionalArgs()
        _INFO(inputFiles)
        general = CLP.getGeneralSettings()
        _INFO(general)
        audio = CLP.getAudioSettings()
        _INFO(audio)
        video = CLP.getVideoSettings()
        _INFO(video)
        transforms = CLP.getTransformSettings()
        _INFO(transforms)

    except Exception as e:
        _ERROR(e)
    #except

    executor.execute(general, audio, video, transforms)

#_main


def mainCut():
    """main routine for av-cut
    """
    executor = execution.Executor(execution.ExecType.CUT)
    _main(executor,
          "cuts out video between two timestamps (no transcoding)")
#mainCut


def mainPlay():
    """main routine for av-play
    """
    executor = execution.Executor(execution.ExecType.PLAY)
    _main(executor,
          "plays video and offers a simplified way of specifying "
          "cropping and scaling parameters")

#mainPlay


def mainToAAC():
    """main routine for av-to-aac
    """
    executor = execution.Executor(execution.ExecType.TOAAC)
    _main(executor,
          "extracts AAC audio from mp4 video")

#mainToAAC


def mainToMp3():
    """main routine for av-to-mp3
    """
    executor = execution.Executor(execution.ExecType.TOMP3)
    _main(executor,
          "extracts audio track from audio or video file and converts it to mp3")

#mainToMp3


def mainToMp4():
    """main routine for av-to-mp4
    """
    executor = execution.Executor(execution.ExecType.TOMP4)
    optionIDs = clp.OptionID.all()
    _main(executor, optionIDs,
          "converts video to mp4 (h.265) using a set of sensible defaults")

#mainToMp4


### aczutro ###################################################################
