#!/bin/bash

# Load environment variables from .env file
source /home/openzyme/.env

VIDEO_PATH="/home/openzyme/videos"
BACKOFF=5
LOG_FILE="/home/openzyme/upload_videos.log"

while true; do
    for file in "$VIDEO_PATH"/*.h264; do
        if [ -f "$file" ]; then
            recorded_at=$(basename "$file" | cut -d'_' -f1)_$(basename "$file" | cut -d'_' -f2 | cut -d'.' -f1)Z
            recorded_at_formatted=$(date -d "${recorded_at:0:8} ${recorded_at:9:4}" "+%Y-%m-%dT%H:%M:%SZ")
            UPLOAD_URL="$SERVER_URL/devices/$DEVICE_REGISTER_ID/upload/"
            
            # Perform the upload
            response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$UPLOAD_URL" \
                -F "secret=$DEVICE_SECRET" \
                -F "file=@$file" \
                -F "recorded_at=$recorded_at_formatted" \
                -F "sensor=camera")

            if [ "$response" -eq 200 ]; then
                echo "$(date '+%Y-%m-%d %H:%M:%S') - Upload successful: $file" >> "$LOG_FILE"
                rm "$file"
                BACKOFF=5
            else
                echo "$(date '+%Y-%m-%d %H:%M:%S') - Upload failed ($response): $file. Retrying in $BACKOFF seconds..." >> "$LOG_FILE"
                sleep $BACKOFF
                BACKOFF=$((BACKOFF * 2))
                if [ $BACKOFF -gt 300 ]; then
                    BACKOFF=300
                fi
            fi
        fi
    done
    sleep 10
done
