This folder contains code that runs on the Raspbian device.


# Device setup instructions
From OS bookworm 

```
$ sudo mkdir /opt/heartbeat
$ sudo mkdir /etc/heartbeat
$ sudo vi /opt/heartbeat/heartbeat.sh 
$ sudo chmod +x /opt/heartbeat/heartbeat.sh
$ sudo vi /etc/heartbeat/.env
$ sudo chmod 600 /etc/heartbeat/.env
$ sudo vi /etc/systemd/system/heartbeat.service
$ sudo systemctl enable heartbeat.service # allow to auto run on restart
$ sudo systemctl start heartbeat.service
$ sudo systemctl status heartbeat.service
```