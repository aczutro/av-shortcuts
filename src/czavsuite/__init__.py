# czavsuite - a suite of useful scripts to serialise FFmpeg jobs
#
# Copyright 2023 - present Alexander Czutro, github@czutro.ch
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

"""A suite of useful scripts to serialise FFmpeg jobs
"""
__author__ = "Alexander Czutro <github@czutro.ch>"
__version__ = "2.0"


from . import application


def _main(appClass):
    """generic main routine

    :param appClass:  application class
    """
    app = appClass()
    app.execute()
#_main


def mainProbe():
    """main routine for av-probe
    """
    _main(application.ApplicationProbe)
#mainCut


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
