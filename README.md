# av-shortcuts

FFmpeg wrapper with a simplified command line.

Copyright 2020 - 2021 Alexander Czutro, github@czutro.ch

## Description

Command line application that provides a more user-friendly
interface to some often-used FFmpeg functionality.

The following five applications are currently available:

* `av-to-aac`: extracts AAC audio from mp4 video.
* `av-to-mp3`: extracts audio track from audio or video file
               and converts it to mp3.
* `av-to-mp4`: converts video to mp4 using a set of sensible defaults.
* `av-cut`:    cuts out video between two timestamps (no transcoding). 
* `av-play`:   plays video and offers a simplified way of specifying
               cropping and scaling parameters.

## Installation

Move the whole package to a location of your preference, for example
`~/.local/lib/av-shortcuts`.

Then, make sure that the main application files are executable, or make
them executable with `chmod +x FILENAME`

The main application files are:

* `~/.local/lib/av-shortcuts/src/av-to-aac`
* `~/.local/lib/av-shortcuts/src/av-to-mp3`
* `~/.local/lib/av-shortcuts/src/av-to-mp4`
* `~/.local/lib/av-shortcuts/src/av-cut`  
* `~/.local/lib/av-shortcuts/src/av-play`

Finally:

1. Either add `~/.local/lib/av-shortcuts/src` to your `PATH` variable,
   e.g. in Bash: `export PATH="$PATH:$HOME/.local/lib/av-shortcuts/src"`
   
2. Or create soft links to the main application files at a location
   that you know is in your `PATH`, e.g. with Bash: `cd ~/.local/bin ;
   ln -s ~/.local/lib/av-shortcuts/src/av-to-mp4.py av-to-mp4`
   
3. Or create shell aliases that invoke the main application files, e.g.
   in Bash: `alias av-to-mp4=~/.local/lib/av-shortcuts/src/av-to-mp4.py`
   or `alias av-to-mp4="python ~/.local/lib/av-shortcuts/src/av-to-mp4.py"` 
