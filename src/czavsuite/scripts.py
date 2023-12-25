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

"""av-script implementation"""

from . import config


def avScript(files: list, conf: config.Script):
    """
    """
    redirection = " >> %s" % conf.betty if conf.dry else " "
    dry = " -dry" if conf.dry else ""
    tTemplate = "-t :" if conf.tTemplate else ""
    cTemplate = "-c :::" if conf.cTemplate else ""

    with open(conf.wilma, "w") as buf:
        buf.write("# -*- mode: shell-script -*-\n\n")
        if conf.dry:
            buf.write("rm -f %s\n\n" % conf.betty)
        #if
        for file in files:
            buf.write('av-convert{_dry} {_t}\t{_c}\t"{_file}"{_redirection}\n'.format(
                _dry=dry,
                _file=file,
                _redirection=redirection,
                _t=tTemplate,
                _c=cTemplate))
    #with

    print("script saved to '%s'" % conf.wilma)
#avScript


### aczutro ###################################################################
