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

"""FFmpeg wrapper"""

from . import config
from czutils.utils import czlogging, cztext
import os.path
import re
import subprocess


_logger = czlogging.LoggingChannel("czavsuite.ffmpeg",
                                   czlogging.LoggingLevel.ERROR,
                                   colour=True)


class FfmpegError(Exception):
    pass


class SystemCaller:

    def __init__(self, exceptionOnFailure: bool):
        self._stdout = ""
        self._stderr = ""
        self._doRaise = exceptionOnFailure
    #__init__


    def stdout(self):
        return self._stdout
    #stdout


    def stderr(self):
        return self._stderr
    #stdout


    def call(self, args: list):
        P = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = P.communicate()
        self._stdout = stdout.decode(errors="ignore")
        self._stderr = stderr.decode(errors="ignore")
        if P.returncode and self._doRaise:
            _logger.warning("'%s'" % " ".join(args), "returned", P.returncode)
            raise FfmpegError(self._stderr)
        #if
        return P.returncode
    #def

#SystemCaller


def _grep(pattern: str, text, ignoreCase=False, colour=False):
    if type(text) is str:
        return _grep(pattern, text.split(sep='\n'), ignoreCase, colour)
    #if

    flags = re.IGNORECASE if ignoreCase else 0
    matcher = re.compile(pattern, flags)
    ans = []
    for line in text:
        if colour:
            match = matcher.search(line)
            if match is not None:
                start, end = match.start(), match.end()
                ans.append("%s%s%s"
                           % (line[:start],
                              cztext.colourise(line[start:end], cztext.Col16.RED, bold=True),
                              line[end:]))
            #if
        else:
            if matcher.search(line) is not None:
                ans.append(line)
            #if
        #else
    #for
    return ans
#grep


def _ffprobeDict(lines: list):
    ans = dict()
    for line in lines:
        tokens = line.split(sep='=')
        if len(tokens) == 2:
            ans[tokens[0]] = tokens[1]
        #if
    #for
    return ans
#_getDict


def ffprobe(file: str, mode: int):
    """
    TODO
    """
    S = SystemCaller(True)

    if mode == config.Probing.FULL:
        returnCode = S.call(['ffprobe', '-hide_banner', file])
        _logger.info("return code:", returnCode)
        _logger.info("stdout:", S.stdout())
        _logger.info("stderr:", S.stderr())
        return _grep("Video|Audio",
                     _grep("Stream", S.stderr()),
                     colour=True)
    elif mode == config.Probing.VIDEO or mode == config.Probing.AUDIO:
        returnCode = S.call(['ffprobe', '-hide_banner',
                             '-show_streams', '-select_streams',
                             'v' if mode == config.Probing.VIDEO else 'a',
                             file])
        _logger.info("return code:", returnCode)
        _logger.info("stdout:", S.stdout())
        _logger.info("stderr:", S.stderr())
        return _ffprobeDict(S.stdout().split(sep='\n'))
    elif mode == config.Probing.DURATION:
        returnCode = S.call(['ffprobe', '-hide_banner', file])
        _logger.info("return code:", returnCode)
        _logger.info("stdout:", S.stdout())
        _logger.info("stderr:", S.stderr())
        return _grep("Duration", S.stderr())[0].split(sep=',')[0].split(sep=' ')[3]
    else:
        raise ValueError
    #else
#ffprobe


def _outputFilename(inputFile: str, outputType: str):
    """
    inputFile: string
    lInputTypes: list of strings
    outputType: string
    Constructs (and returns) a file name by replacing the input file's
    ending by outputType.  The input file's ending must be in lInputTypes.
    """
    tokens = inputFile.split('.')
    outputFile = None

    if len(tokens) == 1:
        return '%s.%s' % (inputFile, outputType)
    else:
        inputType = tokens[-1]
        if inputType == outputType:
            tokens[-2] = tokens[-2] + '-new'
            outputFile = '.'.join(tokens)
        else:
            tokens[-1] = outputType
            outputFile = '.'.join(tokens)
        #else
    #else

    return outputFile
#def


def _checkExistence(filename: str):
    """tests whether a file exists, and if it does,
     asks the user whether to overwrite;
     if user answer yes, removes the file;
     if user answers no, raises an exception"""
    try:
        if os.path.exists(filename):
            if input("file %s already exists -- overwrite? " % filename) in [ 'y', 'Y', 'yes', 'YES' ]:
                os.remove(filename)
            else:
                raise FfmpegError("file %s already exists -- aborting" % filename)
            #if
        #if
    except PermissionError as e:
        raise FfmpegError(e)
    #except
#def


def _toFFmpegVideo(conf: config.Video) -> list:
    codec = ""
    if conf.codec == "h265":
        codec = "libx265"
    elif conf.codec == "h264":
        codec = "libx264"
    elif conf.codec == "null":
        return [ "-vn" ]
    elif conf.codec == "copy":
        return [ "-c:v", "copy" ]
    else:
        raise ValueError
    #else
    return [ "-c:v", codec, "-crf", conf.crf ]
#_toFFmpegVideo


def _toFFmpegAudio(conf: config.Audio) -> list:
    if conf.codec == "aac":
        codec = [ "-c:a", "aac" ]
        if conf.bitrate is not None:
            return codec + [ "-b:a", conf.bitrate ]
        else:
            return codec
        #if
    elif conf.codec == "mp3":
        codec = [ "-c:a", "libmp3lame" ]
        if conf.bitrate is not None and conf.quality is not None:
            raise ValueError
        elif conf.bitrate is not None:
            return codec + [ "-b:a", conf.bitrate ]
        elif conf.quality is not None:
            return codec + [ "-q:a", conf.quality ]
        else:
            return codec
        #if
    elif conf.codec == "null":
        return [ "-an" ]
    elif conf.codec == "copy":
        return [ "-c:a", "copy" ]
    else:
        raise ValueError
    #else
#_toFFmpegVideo


def _toFFmpegCropping(conf: config.Cropping) -> list:
    if conf.valid:
        return [ '-vf', 'crop=in_w-%s:in_h-%s:%s:%s' %
                 (conf.left + conf.right, conf.up + conf.down, conf.left, conf.up) ]
    else:
        return []
    #else
#_toFFmpegCropping


def _toFFmpegScaling(file: str, conf: config.Scaling) -> list:
    if conf.valid:
        probe = ffprobe(file, config.Probing.VIDEO)
        width = int(probe["width"])
        height = int(probe["height"])
        fWidth = width * conf.factor
        fHeight = height * conf.factor
        width = int(fWidth) + int(fWidth) % 2
        height = int(fHeight) + int(fHeight) % 2
        return [ '-vf', 'scale=%d:%d' % (width, height) ]
    else:
        return []
    #else
#_toFFmpegScaling


def _toFFmpegCuttting(conf: config.Cutting) -> list:
    if conf.valid:
        diff = conf.end - conf.start
        if diff <= 0:
            raise ValueError
        #if
        return [ "-ss", str(conf.start), "-t", str(diff) ]
    else:
        return []
    #else
#_toFFmpegCuttting


def avToMp4(files: list,
            confGeneral: config.General,
            confVideo: config.Video,
            confAudio: config.Audio,
            confCropping: config.Cropping,
            confCutting: config.Cutting,
            confScaling: config.Scaling):
    S = SystemCaller(True)
    for file in files:
        outputFile = _outputFilename(file, "mp4")
        _checkExistence(outputFile)
        cmd = ([ 'ffmpeg', '-hide_banner', '-i', file ] + _toFFmpegCropping(confCropping) +
               _toFFmpegScaling(file, confScaling) + _toFFmpegVideo(confVideo) +
               _toFFmpegAudio(confAudio) + _toFFmpegCuttting(confCutting) + [ outputFile ])
        print(" ".join(cmd))
        if not confGeneral.dry:
            returnCode = S.call(cmd)
            _logger.info("return code:", returnCode)
            _logger.info("stdout:", S.stdout())
            _logger.info("stderr:", S.stderr())
            print(S.stderr())
            print("=======================")
        #if
    #for
#avToMp4
