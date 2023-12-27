# av-shortcuts

A suite of useful scripts to serialise FFmpeg jobs.

Copyright (C) 2020 - present  Alexander Czutro <github@czutro.ch>

Licence: GNU GPL v3

## Description

This suite of scripts was born out of the necessity to process large numbers of
videos with FFmpeg.  However, FFmpeg's command line interface is a lot more 
complex than it needs to be for most jobs, and it can only process one job per 
command line.  

The following applications are FFmpeg wrappers that will help you perform some
common jobs with little typing.

### av-probe

This is an `ffprobe` wrapper.  Unlike `ffprobe`, it allows you to process
several files with one command, and it has three modes to give you an
easy-to-read (and parse) overview of the most relevant data.
For example, the `-v` flag will produce an output like this:

    codec  resolution  aspect ratio  fps    file
    -----  ----------  ------------  ---    ----
    vp9    1920x1080   16:9          23.98  some-video-1.webm
    vp9    638x480     319:240       29.97  some-video-2.webm
    vp9    854x480     427:240       29.97  some-video-3.webm
    vp9    1920x1080   16:9          59.94  some-video-4.webm
    vp9    1920x1080   16:9          23.98  some-video-5.webm
    vp9    1920x1080   16:9          29.97  some-video-6.webm
    vp9    1920x1080   16:9          29.97  some-video-7.webm
    null   --          --            --     some-audio.m4a

### av-play

This is an `ffplay` wrapper.  Unlike `ffplay`, you can specify any number of 
files to play.  It supports video cropping, video scaling and timeline cutting.

### av-convert

This converts audio or video files to mp4, m4a or mp3 files.  It allows you to 
choose between AVC and HEVC for video and MP3 or AAC for audio, and to set video 
and audio quality with a very easy-to-use command line interface.  It also
supports video cropping, video scaling and timeline cutting.

### av-script

This produces a script template for when you need to run several `av-convert`
jobs with individual job settings.  You can use `czmake` (library `czutils`, 
which is needed by `czavsuite`, so you will have to install it anyway) to turn 
that script into a Makefile, so it's easier to keep track of failed conversion 
jobs.

### av-rename

This script identifies pairs of files that have been converted using
`av-convert` (the “before” and the “after” file), moves them to a target
directory and renames them such that the before files are hidden.

### av-classify

A little helper for when you want to classify video files and you have to watch
them to see what's actually in them.  Also works with images.

## Installation

1. Make sure that you have installed FFmpeg on your system, and that `ffmpeg`,
   `ffplay` and `ffprobe` are callable (in your PATH variable).

2. Change into the distribution's root directory (where the `pyproject.toml`
   file is located).

3. Run `pip install .` 
