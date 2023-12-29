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
__version__ = "2.0.1"


from . import application


def mainProbe():
    """entry point for av-probe
    """
    application.ApplicationProbe()
#mainCut


def mainConvert():
    """entry point for av-convert
    """
    application.ApplicationConvert()
#mainToMp4


def mainPlay():
    """entry point for av-play
    """
    application.ApplicationPlay()
#mainPlay


def mainScript():
    """entry point for av-script
    """
    application.ApplicationScript()
#mainScript


def mainClassify():
    """entry point for av-classify
    """
    application.ApplicationClassify()
#mainClassify


def mainRename():
    """entry point for av-rename
    """
    application.ApplicationRename()
#mainRename


### aczutro ###################################################################
