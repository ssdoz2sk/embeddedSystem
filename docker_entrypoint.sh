#!/bin/sh

if [ ! -f "/web/config/secret.key" ]; then
    echo $(cat /dev/urandom | tr -dc 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(\-_=+)' | fold -w 50 | head -n 1) > "/web/config/secret.key"
fi

python manage.py migrate --no-input

uwsgi /web/config/embeddedSystem.ini

nginx -g 'daemon off;'

