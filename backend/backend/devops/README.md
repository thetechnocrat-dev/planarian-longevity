```
sudo vim /etc/systemd/system/gunicorn.service
sudo touch /var/log/gunicorn_access.log /var/log/gunicorn_error.log
sudo chown ubuntu:www-data /var/log/gunicorn_*.log
sudo chmod 775 /var/log/gunicorn_*.log
sudo mkdir -p /var/log/planarian-longevity
sudo chown ubuntu:www-data /var/log/planarian-longevity
sudo chmod 775 /var/log/planarian-longevity
sudo touch /var/log/planarian-longevity/django_errors.log
sudo chown ubuntu:www-data /var/log/planarian-longevity/django_errors.log
sudo chmod 775 /var/log/planarian-longevity/django_errors.log
sudo vim /etc/logrotate.d/planarian-longevity
```
