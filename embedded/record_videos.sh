#!/bin/bash

VIDEO_DIR="/home/openzyme/videos"
mkdir -p $VIDEO_DIR

while true; do
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    FILENAME="${VIDEO_DIR}/${TIMESTAMP}_camera.h264"
    rpicam-vid -t 60000 --framerate 30 --width 1640 --height 1232 -o $FILENAME
done
