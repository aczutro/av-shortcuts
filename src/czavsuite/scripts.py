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

from . import config, utils
import os
import shutil


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


def avClassify(files: list, conf: config.Classify):
    """
    """
    S = utils.SystemCaller(False)
    if conf.images:
        cmd = [ 'feh', '-g', '+1280+0' ]
        if os.environ.get('AV_CLASS_VIEWER') is not None:
            cmd = os.environ.get('AV_CLASS_VIEWER').split(sep=' ')
        #if
    else:
        cmd = [ 'mplayer', '-geometry', '+1280+0' ]
        if conf.mute:
            cmd += [ '-ao', 'null' ]
        #if
        if os.environ.get('AV_CLASS_PLAYER') is not None:
            cmd = os.environ.get('AV_CLASS_PLAYER').split(sep=' ')
        #if
    #else
    for file in files:
        S.call(cmd + [file])
        try:
            target = ".%s" % input("%s: " % file)
        except EOFError:
            break
        #except
        if target == ".":
            continue
        #if
        try:
            os.mkdir(target)
        except FileExistsError as e:
            if not os.path.isdir(target):
                raise e
            #if
        #except
        shutil.move(file, target)
    #for
#avClassify


### aczutro ###################################################################
