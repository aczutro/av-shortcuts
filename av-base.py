#!/usr/bin/python3
#
# av-shortcuts - FFmpeg wrapper with a simplified command line
#
# Copyright 2020 Alexander Czutro
#
# github@czutro.ch
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

from sys import argv as __argv
from os import \
    remove as _rm
from os.path import \
    basename as _basename, \
    exists as _exists
from subprocess import \
    Popen as _child, \
    PIPE as _pipe


class App:
    toAAC = 'av-to-aac'
    toMP3 = 'av-to-mp3'
    toMP4 = 'av-to-mp4'
    play = 'av-play'
    cut = 'av-cut'
#App


class Opt:
    ab = 'ab'
    aq = 'aq'
    mp3 = 'mp3'
    aac = 'aac'
    noaudio = 'noa'
    copyaudio = 'copya'
    crf = 'crf'
    dry = 'dry'
    crop = 'c'
    time = 't'
    scale = 's'
#Opti


class Key:
    ab, aq, acodec, crf, dry, crop, scale, time = range(8)
#Key


class MainClass:

    def __init__(self, _appName, _lFiles, _lOptions):
        self.appName = _appName
        self.lFiles = _lFiles
        self.lOptions = _lOptions
        self.execMap = {
            App.toAAC : self.avToAac,
            App.toMP3 : self.avToMp3,
            App.toMP4 : self.avToMp4,
            App.play  : self.avPlay,
            App.cut   : self.avCut
        }
        self.D = dict()
        self.D[Key.acodec] = 'aac'
    #def


    def execute(self):
        if self.appName in self.execMap:
            self.execMap[self.appName]()
        else:
            raise Exception("don't know what to do")
        #else
    #def


    def systemCall(self, *args):
        """Runs a non-interactive sub-process and
        returns its outputs and exit code."""
        P = _child(args, stdin=None, stdout=_pipe, stderr=_pipe)
        stdout, stderr = P.communicate()
        if P.returncode:  # command failed
            raise Exception(stderr.decode())
        else:
            print(stderr.decode())
            return stdout.decode()
        #else
    #def


    def makeCropString(self, _left, _right, _up, _down):
        left = int(_left)
        right = int(_right)
        up = int(_up)
        down = int(_down)
        return 'crop=in_w-%s:in_h-%s:%s:%s' % (left + right, up + down, left, up)
    #def


    def makeScaleString(self, inputFile, _scaleFactor):
        scaleFactor = float(_scaleFactor)
        probe = self.systemCall('ffprobe', inputFile, '-show_entries', 'stream=width,height').split()
        width, height = None, None
        for line in probe:
            tokens = line.split(sep='=')
            if len(tokens) == 2:
                if tokens[0] == 'width':
                    width = int(tokens[1])
                #if
                if tokens[0] == 'height':
                    height = int(tokens[1])
                #if
            #if
        #for
        if None in [ width, height ]:
            raise Exception('ffprobe failed')
        #if
        fWidth = width * scaleFactor
        fHeight = height * scaleFactor
        if int(fWidth) % 2:
            width = int(fWidth) + 1
        else:
            width = int(fWidth)
        #else
        if int(fHeight) % 2:
            height = int(fHeight) + 1
        else:
            height = int(fHeight)
        #else
        return [ '-vf', 'scale=%d:%d' % (width, height) ]
    #def


    def scanOptions(self):
        for option, argument in lOptions:
            if option == Opt.ab:
                self.D[Key.ab] = argument
            elif option == Opt.aq:
                self.D[Key.aq] = argument
            elif option == Opt.mp3:
                self.D[Key.acodec] = 'libmp3lame'
            elif option == Opt.aac:
                self.D[Key.acodec] = 'aac'
            elif option == Opt.copyaudio:
                self.D[Key.acodec] = 'copy'
            elif option == Opt.noaudio:
                del self.D[Key.acodec]
            elif option == Opt.crf:
                self.D[Key.crf] = argument
            elif option == Opt.dry:
                self.D[Key.dry] = None
            elif option == Opt.crop:
                cropArgs = argument.split(':')
                if len(cropArgs) == 2:
                    self.D[Key.crop] = self.makeCropString(
                        cropArgs[0], cropArgs[0], cropArgs[1], cropArgs[1])
                else:
                    self.D[Key.crop] = self.makeCropString(*cropArgs)
                #else
            elif option == Opt.scale:
                self.D[Key.scale] = argument
            elif option == Opt.time:
                fromTime, toTime = argument.split(':')
                startTime, lengthTime = None, None
                if not len(fromTime) + len(toTime):  # -t::
                    raise Exception('-t: from and to MUST not be both empty')
                elif len(fromTime) * len(toTime):  # -t:from:to
                    if float(fromTime) != 0:
                        startTime = fromTime
                    #if
                    lengthTime = str(float(toTime) - float(fromTime))
                elif fromTime:  # -t:from:
                    if float(fromTime):
                        startTime = fromTime
                    #if
                else:  # -t::to
                    lengthTime = toTime
                #else
                self.D[Key.time] = []
                if startTime:
                    self.D[Key.time].extend(['-ss', startTime])
                # if
                if lengthTime:
                    self.D[Key.time].extend(['-t', lengthTime])
                # if
            else:
                raise Exception('unrecognised option: %s' % option)
            #else
        #for
    #scanOptions


    def deriveOutputName(self, inputFile, lInputTypes, outputType):
        """
        inputFile: string
        lInputTypes: list of strings
        outputType: string
        Constructs (and returns) a file name by replacing the input file's
        ending by outputType.  The input file's ending must be in lInputTypes.
        """
        lTokens = inputFile.split('.')
        outputFile = None

        if len(lTokens) == 1:  # no file ending
            # in this version, not caring about file name extension
            #todo: find out file type based on content
            return '%s.%s' % (inputFile, outputType)
        else:
            inputType = lTokens[-1]
            if inputType not in lInputTypes:
                raise Exception('%s: unrecognised file name extension: %s' % (inputFile, inputType))
            elif inputType == outputType:
                lTokens[-2] = lTokens[-2] + '-new'
                outputFile = '.'.join(lTokens)
            else:
                lTokens[-1] = outputType
                outputFile = '.'.join(lTokens)
            #else
        #else

        #print(inputFile, '->', outputFile)

        return outputFile
    #def


    def testExistence(self, filename):
        """tests whether a file exists, and if it does,
         asks the user whether to overwrite;
         if user answer yes, removes the file;
         if user answers no, raises an exception"""
        if _exists(filename):
            if input("file %s already exists -- overwrite? " % filename) in [ 'y', 'Y', 'yes', 'YES' ]:
                _rm(filename)
            else:
                raise Exception("file %s already exists -- aborting" % filename)
            #if
        #if
    #def


    def avToAac(self):
        """extracts aac stream from each input file"""
        for inputFile in self.lFiles:
            outputFile = self.deriveOutputName(inputFile, ['mp4'], 'aac')
            self.testExistence(outputFile)
            self.systemCall('ffmpeg', '-i', inputFile, '-c:a', 'copy', outputFile)
        #for
    #avExtractAac


    def avToMp3(self):
        """extracts audio stream from each input file and converts it to mp3"""
        self.scanOptions()
        for inputFile in self.lFiles:
            outputFile = self.deriveOutputName(inputFile, ['mp4', 'wav', 'mp3', 'aac'], 'mp3')
            self.testExistence(outputFile)
            command = [ 'ffmpeg', '-i', inputFile ]  # , '-c:a', 'libmp3lame' ]
            if Key.ab in self.D:
                command.extend([ '-b:a', self.D[Key.ab] ])
            elif Key.aq in self.D:
                command.extend([ '-q:a', self.D[Key.aq] ])
            else:
                command.extend([ '-q:a', '0' ])
            #else
            command.append(outputFile)
            self.systemCall(*command)
        #for
    #avExtractAac

    def avToMp4(self):
        """converts to mp4 with h.265 video and aac or mp3 audio"""
        self.scanOptions()
        if Key.crop in self.D and Key.scale in self.D:
            raise Exception('-c cannot be combined with -s')
        #if
        for inputFile in self.lFiles:
            outputFile = self.deriveOutputName(inputFile, ['avi', 'wmv', 'mov', 'mpg', 'mp4', 'ogv', 'flv'], 'mp4')
            self.testExistence(outputFile)
            command = [ 'ffmpeg', '-i', inputFile ]
            if Key.crop in self.D:
                command.extend([ '-vf', self.D[Key.crop] ])
            #if
            if Key.scale in self.D:
                command.extend(self.makeScaleString(inputFile, self.D[Key.scale]))
            #if
            command.extend([ '-c:v', 'libx265' ])
            if Key.crf in self.D:
                command.extend([ '-crf', self.D[Key.crf] ])
            else:
                command.extend([ '-crf', "23" ])
            #if
            if Key.acodec in self.D:
                command.extend([ '-c:a', self.D[Key.acodec] ])
            else:
                command.append('-an')
            #else
            if Key.ab in self.D:
                command.extend([ '-b:a', self.D[Key.ab] ])
            elif Key.acodec in self.D and self.D[Key.acodec] == 'libmp3lame':
                command.extend([ '-q:a', '0' ])
            #if
            if Key.time in self.D:
                command.extend(self.D[Key.time])
            #if
            command.append(outputFile)
            print(' '.join(command))
            if Key.dry not in self.D:
                print(self.systemCall(*command))
                print("=======================")
            #if
        #for
    #avToMp4


    def avCut(self):
        """cuts out a section of video without transcoding"""
        self.scanOptions()
        if Key.time not in self.D:
            raise Exception('-t is required')
        #if
        for inputFile in self.lFiles:
            outputFile = self.deriveOutputName(inputFile, ['mp4'], 'mp4')
            self.testExistence(outputFile)
            command = [ 'ffmpeg', '-i', inputFile, '-c', 'copy' ] + self.D[Key.time] + [ outputFile ]
            self.systemCall(*command)
        #for
    #avCut

    def avPlay(self):
        self.scanOptions()
        if Key.crop in self.D and Key.scale in self.D:
            raise Exception('-c cannot be combined with -s')
        #if
        for inputFile in self.lFiles:
            command = [ 'ffplay', inputFile ]
            if Key.crop in self.D:
                command.extend([ '-vf', self.D[Key.crop] ])
            #if
            if Key.scale in self.D:
                command.extend(self.makeScaleString(inputFile, self.D[Key.scale]))
            #if
            if Key.time in self.D:
                command.extend(self.D[Key.time])
            #if
            self.systemCall(*command)
        #for
    #avExtractAac

#MainClass


# main ------------------------------------------------------------------------

if __name__ == '__main__':

    if len(__argv) == 1:
        print('''
%s FILE ...
    extracts audio stream from files and converts it to aac

%s [ -%s:BITRATE ] [ -%s:QUALITY ] FILE ...
    extracts audio stream from files and converts it to mp3;
    default is vbr with highest quality (0)

%s [ OPTIONS ] FILE ...
    options:
        -%s
            don't do anything; only print ffmpeg command line
        -%s | -%s | -%s | -%s
            choose audio codec; default is AAC
        -%s:AUDIOBITRATE
            aac default is ffmpeg's default;
            mp3 default is vbr with highest quality
        -%s:CRF
            default video quality is ffmpeg's default
        -%s:CROP_LEFT[:CROP_RIGHT]:CROP_UP[:CROP_DOWN]
        -%s:SCALE_FACTOR
        -%s:FROM:TO
            FROM or TO may be empty

%s -%s:FROM:TO FILE ...

%s [ OPTIONS ] FILE ...
    options:
        -%s:CROP_LEFT[:CROP_RIGHT]:CROP_UP[:CROP_DOWN]
        -%s:SCALE_FACTOR
        -%s:FROM:TO
            FROM or TO may be empty
''' % (
            App.toAAC,
            App.toMP3, Opt.ab, Opt.aq,
            App.toMP4,
            Opt.dry,
            Opt.aac, Opt.mp3, Opt.noaudio, Opt.copyaudio,
            Opt.ab,
            Opt.crf,
            Opt.crop,
            Opt.scale,
            Opt.time,
            App.cut, Opt.time,
            App.play,
            Opt.crop,
            Opt.scale,
            Opt.time
        ))
        exit(1)
    # if

    appName = _basename(__argv[0])
    # appName = App.play # for debugging

    lFiles = []
    lOptions = []

    for token in __argv[1:]:
        if token[0] == '-':
            optionTokens = token[1:].split(':')
            if not optionTokens:
                print('%s: unrecognised option: -', appName)
                exit(2)
            #if
            lOptions.append((optionTokens[0], ':'.join(optionTokens[1:])))
        else:
            lFiles.append(token)
        #else
    #for

    M = MainClass(appName, lFiles, lOptions)

    try:
        M.execute()
        exit(0)
    except Exception as e:
        print('%s: %s' % (appName, e))
        exit(3)
    #except
#main
