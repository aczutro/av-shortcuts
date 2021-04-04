# av-shortcuts - FFmpeg wrapper with a simplified command line
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

"""FFmpeg wrapper with a simplified command line
"""
__author__ = "Alexander Czutro, github@czutro.ch"


from . import application


def _main(appClass):
    """generic main routine

    :param appClass:  application class
    """
    app = appClass()
    app.parseCommandLine()
    app.execute()
#_main


def mainCut():
    """main routine for av-cut
    """
    _main(application.ApplicationCut)
#mainCut


def mainPlay():
    """main routine for av-play
    """
    _main(application.ApplicationPlay)
#mainPlay


def mainToAAC():
    """main routine for av-to-aac
    """
    _main(application.ApplicationToAAC)
#mainToAAC


def mainToMp3():
    """main routine for av-to-mp3
    """
    _main(application.ApplicationToMp3)
#mainToMp3


def mainToMp4():
    """main routine for av-to-mp4
    """
    _main(application.ApplicationToMp4)
#mainToMp4


### aczutro ###################################################################
