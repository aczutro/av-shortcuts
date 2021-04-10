# av-shortcuts

FFmpeg wrapper with a simplified command line.

Copyright (C) 2020 - present  Alexander Czutro <github@czutro.ch>

Licence: GNU GPL v3

## Description

Command line applications that provide a more user-friendly
interface to some often-used FFmpeg functionality.

The following five applications are currently available:

* `av-to-aac`: extracts AAC audio from video files.
* `av-to-mp3`: extracts audio track from audio or video file
               and converts it to mp3.
* `av-to-mp4`: converts video to mp4 (h.265) using a set of sensible 
               defaults.
* `av-cut`:    cuts out video between two timestamps (no transcoding). 
* `av-play`:   plays video and offers a simplified way of specifying
               cropping and scaling parameters.

## Installation

In the root directory of this distribution you will find the following
files and directories:

* `bin/` -- the directory with the main executables
* `src/` -- the directory with the library files
* `setup.cfg` -- setup file for the installation
* `setup.py` -- setup script for the installation

To install, do the following:

1. Change into the root directory.

2. Run the following command (no need to be root): `python -m pip install .`

3. Copy or move the main executables to a location that you know is in your
   `PATH`, e.g. `~/.local/bin`.  Or create a symbolic link:
   ```shell
   cd ~/.local/bin ; ln -s /path/to/distribution/bin/av-to-mp4.py av-to-mp4
   ```
