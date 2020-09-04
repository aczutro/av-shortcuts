#!/usr/bin/python3
#
# aczutro
#
# Sun Mar 29 19:22:21 CEST 2020
#
###############################################################################

from sys import argv as __argv
from os.path import \
    basename as _basename, \
    exists as _exists
from subprocess import \
    Popen as _child, \
    PIPE as _pipe, \
    call as _call


class App:
    toAAC = 'av-to-aac'
    toMP3 = 'av-to-mp3'
    toMP4 = 'av-to-mp4'
    play = 'av-play'
#App


class Opt:
    ab = 'ab'
    aq = 'aq'
    mp3 = 'mp3'
    aac = 'aac'
    vq = 'vq'
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
            App.play : self.avPlay
        }
        self.D = dict()
    #def


    def execute(self):
        if self.appName in self.execMap:
            self.execMap[self.appName]()
        else:
            raise Exception("don't know what to do")
        #else
    #def


    def systemCall(self, *args):
        '''Runs a non-interactive sub-process and
        returns its outputs and exit code.'''
        print(' '.join(args))
        P = _child(args, stdin=None, stdout=_pipe, stderr=_pipe)
        stdout, stderr = P.communicate()
        if P.returncode: # command failed
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
            elif option == Opt.vq:
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
                if not len(fromTime) + len(toTime): # -t::
                    raise Exception('-t: from and to MUST not be both empty')
                elif len(fromTime) * len(toTime): # -t:from:to
                    if float(fromTime) != 0:
                        startTime = fromTime
                    #if
                    lengthTime = str(float(toTime) - float(fromTime))
                elif fromTime: # -t:from:
                    if float(fromTime):
                        startTime = fromTime
                    #if
                else: # -t::to
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
        '''
        inputFile: string
        lInputTypes: list of strings
        outputType: string
        Constructs (and returns) a file name by replacing the input file's
        ending by outputType.  The input file's ending must be in lInputTypes.
        '''
        lTokens = inputFile.split('.')
        outputFile = None

        if len(lTokens) == 1: # no file ending
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

        print(inputFile, '->', outputFile)
        return outputFile
    #def


    def avToAac(self):
        '''extracts aac stream from each input file'''
        for inputFile in self.lFiles:
            outputFile = self.deriveOutputName(inputFile, ['mp4'], 'aac')
            if _exists(outputFile):
                raise Exception("file %s already exists -- aborting" % outputFile)
            #if
            self.systemCall('ffmpeg', '-i', inputFile, '-c:a', 'copy', outputFile)
        #for
    #avExtractAac


    def avToMp3(self):
        '''extracts audio stream from each input file and converts it to mp3'''
        self.scanOptions()
        for inputFile in self.lFiles:
            outputFile = self.deriveOutputName(inputFile, ['mp4', 'wav', 'mp3', 'aac'], 'mp3')
            if _exists(outputFile):
                raise Exception("file %s already exists -- aborting" % outputFile)
            #if
            command = [ 'ffmpeg', '-i', inputFile ] #, '-c:a', 'libmp3lame' ]
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
        '''converts to mp4 with h.264 video and aac or mp3 audio'''
        self.scanOptions()
        if Key.crop in self.D and Key.scale in self.D:
            raise Exception('-c cannot be combined with -s')
        #if
        for inputFile in self.lFiles:
            outputFile = self.deriveOutputName(inputFile, ['avi', 'wmv', 'mov', 'mpg', 'mp4', 'ogv'], 'mp4')
            if _exists(outputFile):
                raise Exception("file %s already exists -- aborting" % outputFile)
            #if
            command = [ 'ffmpeg', '-i', inputFile ]
            if Key.crop in self.D:
                command.extend([ '-vf', self.D[Key.crop] ])
            #if
            if Key.scale in self.D:
                command.extend(self.makeScaleString(inputFile, self.D[Key.scale]))
            #if
            command.extend([ '-c:v', 'libx264' ])
            if Key.acodec in self.D:
                command.extend([ '-c:a', self.D[Key.acodec] ])
            else:
                command.append('-an')
            #else
            if Key.crf in self.D:
                command.extend([ '-crf', self.D[Key.crf] ])
            #if
            if Key.ab in self.D:
                command.extend([ '-b:a', self.D[Key.ab] ])
            elif Key.acodec in self.D and self.D[Key.acodec] == 'libmp3lame':
                command.extend([ '-q:a', '0' ])
            #if
            if Key.time in self.D:
                command.extend(self.D[Key.time])
            #if
            command.append(outputFile)
            if Key.dry in self.D:
                print(' '.join(command))
            else:                
                self.systemCall(*command)
            #else
        #for
    #avToMp4

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
        -%s | -%s
            choose audio codec; if none chosen, produce NO audio
        -%s:AUDIOBITRATE
            aac default is ffmpeg's default;
            mp3 default is vbr with highest quality
        -%s:CRF
            default video quality is ffmpeg's default
        -%s:CROP_LEFT[:CROP_RIGHT]:CROP_UP[:CROP_DOWN]
        -%s:SCALE_FACTOR
        -%s:FROM:TO
            FROM or TO may be empty

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
            Opt.aac, Opt.mp3,
            Opt.ab,
            Opt.vq,
            Opt.crop,
            Opt.scale,
            Opt.time,
            App.play,
            Opt.crop,
            Opt.scale,
            Opt.time
        ))
        exit(1)
    # if

    appName = _basename(__argv[0])
    #appName = App.play # for debugging

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
