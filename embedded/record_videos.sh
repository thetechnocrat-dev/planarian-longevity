#!/bin/bash

VIDEO_DIR="/home/openzyme/videos"
mkdir -p $VIDEO_DIR

while true; do
    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    H264_FILENAME="${VIDEO_DIR}/${TIMESTAMP}_camera.h264"
    MP4_FILENAME="${VIDEO_DIR}/${TIMESTAMP}_camera.mp4"

    # Record video in H.264 format
    rpicam-vid -t 60000 --framerate 15 --width 1640 --height 1232 -o $H264_FILENAME

    # Wrap H.264 in MP4 container
    ffmpeg -i $H264_FILENAME -c copy $MP4_FILENAME

    # Remove the original H.264 file to save space
    rm $H264_FILENAME
done
