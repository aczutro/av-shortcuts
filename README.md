# av-shortcuts
FFmpeg wrapper with a simplified command line

## Description

Provides simplified access to FFmpeg's most commonly used functionality and
options.

## Installation

Copy file `av-base.py` to a location of your preference,
e.g. `/path/to/av-base.py`, and make it executable
(`chmod +x /path/to/av-base.py`).

Then, create symbolic links to `/path/to/av-base.py` in a location that is in
your $PATH variable, e.g.:

```
cd /usr/bin
ln -s /path/to/av-base.py av-play
```

The following five flavours are currently available:

* `av-to-aac`: extracts AAC audio from mp4 video.
* `av-to-mp3`: extracts audio track from video and converts it to mp3.
* `av-to-mp4`: converts video to mp4 using a set of sensible defaults.
* `av-cut`:    cuts out video at the beginning and the end (no transcoding). 
* `av-play`:   plays video and offers a simplified way of specifying cropping
               and scaling paramaters.
