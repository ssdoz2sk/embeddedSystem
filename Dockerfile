FROM python:3.6.6-stretch

ADD . /web

RUN apt-get update && apt-get install -y nginx openssl libmariadbclient-dev

RUN git clone --branch dist https://github.com/ssdoz2sk/embeddedSystemFE.git /web/static

RUN pip install --no-cache-dir -r /web/requirements.txt && \
    pip install --no-cache-dir uwsgi && \
    mkdir /var/log/uwsgi && chown www-data:www-data /var/log/uwsgi && \
    cp -f /web/config/nginx.conf /etc/nginx/nginx.conf && \
    cp -f /web/embeddedSystem/settings.docker.py /web/embeddedSystem/settings.py && \
    /usr/sbin/nginx -t && \
    chmod +x /web/docker_entrypoint.sh


WORKDIR /web

EXPOSE 80

ENTRYPOINT /web/docker_entrypoint.sh
