# planarian longevity
tools for observing planarian

[Hackaday Project Page](https://hackaday.io/project/195642-decentralized-monitoring-of-planarian-regeneration)

## Instructions
On a Raspberry PI with Camera module V2 with Bookworm OS, the following command will take a full field of view video

```
$ rpicam-vid -t 3000 --framerate 30 --width 1640 --height 1232 -o yourfile.h264
```
