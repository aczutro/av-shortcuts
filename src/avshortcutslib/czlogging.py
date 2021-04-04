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

"""logging"""

import logging
import os.path
import sys


class Logger:
    """A wrapper for the system logger which extends info, warning and error
    to accept a variable number of arguments.
    """

    def __init__(self, _level: str):
        """constructor

        :param _level:  minimum level to log
        """
        logging.basicConfig(format="%(name)s: %(cln)s: %(message)s",
                            level=_level)
        self.logger = logging.getLogger(os.path.basename(sys.argv[0]))
    #__init__


    def info(self, *args):
        """Log a message with level INFO on system logger.
        """
        self._log(self.logger.info,
                  ' '.join((str(arg) for arg in args)),
                  "info")
    #info


    def warning(self, *args):
        """Log a message with level WARNING on system logger.
        """
        self._log(self.logger.warning,
                  ' '.join((str(arg) for arg in args)),
                  "warning")
    #warning


    def error(self, *args):
        """Log a message with level ERROR on system logger.
        """
        self._log(self.logger.error,
                  ' '.join((str(arg) for arg in args)),
                  "error")
    #error


    def _log(self, f, msg: str, levelName: str):
        """back-end for logging functions

        :param f:         pointer to function to call
        :param msg:       message to log
        :param levelName: custom level name to use instead of system standard
        """
        f(msg, extra={ "cln" : levelName }) # cln: custom level name
    #_log

#Logger


def initLogging(level: str = "WARNING"):
    """Initialises logging.

    :param level: minimum level to log

    :return: triple composed of function pointers for info, warning and
             error.
    """
    logger = Logger(level)

    return logger.info, logger.warning, logger.error

#initLogging


### aczutro ###################################################################
