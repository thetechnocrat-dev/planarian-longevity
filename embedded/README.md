This folder contains code that runs on the Raspbian device.


# Device setup instructions
From OS bookworm 

```
sudo apt-get update
sudo apt-get -y install git python3-flask ffmpeg
vi /home/openzyme/.env
sudo vi /etc/NetworkManager/system-connections/accesspoint.nmconnection
sudo chmod 600 /etc/NetworkManager/system-connections/accesspoint.nmconnection
sudo vi /etc/NetworkManager/system-connections/tufts_wireless.nmconnection
sudo chmod 600 /etc/NetworkManager/system-connections/tufts_wireless.nmconnection
sudo vi /etc/NetworkManager/NetworkManager.conf
git clone https://github.com/thetechnocrat-dev/planarian-longevity.git
cp -r planarian-longevity/embedded/webapp ./
chmod 600 ./webapp/app.py
sudo vi /etc/systemd/system/webapp.service
sudo systemctl enable webapp.service
sudo systemctl start webapp.service
mkdir /home/openzyme/scripts
vi /home/openzyme/scripts/power_leds.py
chmod +x /home/openzyme/scripts/power_leds.py
sudo vi /etc/systemd/system/power_leds.service
sudo systemctl enable power_leds.service
sudo systemctl start power_leds.service
sudo mkdir /opt/heartbeat
sudo mkdir /etc/heartbeat
sudo vi /opt/heartbeat/heartbeat.sh 
sudo chmod +x /opt/heartbeat/heartbeat.sh
sudo vi /etc/heartbeat/.env
sudo chmod 600 /etc/heartbeat/.env
sudo vi /etc/systemd/system/heartbeat.service
sudo systemctl enable heartbeat.service
sudo systemctl start heartbeat.service
vi /home/openzyme/scripts/record_videos.sh
chmod +x /home/openzyme/scripts/record_videos.sh
vi /home/openzyme/scripts/upload_videos.sh
chmod +x /home/openzyme/scripts/upload_videos.sh
sudo vi /etc/systemd/system/record_videos.service
sudo systemctl enable record_videos.service
sudo systemctl start record_videos.service
sudo vi /etc/systemd/system/upload_videos.service
sudo systemctl enable upload_videos.service
sudo systemctl start upload_videos.service
```

# Webapp
http://192.168.50.1:8080/

# Camera Test
```
rpicam-vid -t 3000 --framerate 30 --width 1640 --height 1232 -o yourfile.h264
```

# Debugging 
```
sudo systemctl status heartbeat.service
```
