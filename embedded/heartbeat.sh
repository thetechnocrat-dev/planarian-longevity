#!/bin/bash

# source ./.env
source /etc/heartbeat/.env

HEARTBEAT_URL="${SERVER_URL}/devices/${DEVICE_REGISTER_ID}/heartbeat/"

while true; do
  response=$(curl -s -o /dev/null -w "%{http_code}" -X POST -d "secret=$DEVICE_SECRET" $HEARTBEAT_URL)
  if [ "$response" -eq 200 ]; then
    echo "Heartbeat updated successfully"
  else
    echo "Failed to update heartbeat, status code: $response"
  fi
  sleep 30  # Wait for 30 seconds before sending the next heartbeat
done
