FROM nginx
COPY default.conf /etc/nginx/conf.d/default.conf
COPY ./html /usr/share/nginx/html
COPY ./cert.conf /tmp
RUN openssl req -x509 -nodes -days 3560 -newkey rsa:4096 -keyout /etc/ssl/private/cdp.key -out /etc/ssl/certs/cdp.crt -config /tmp/cert.conf
EXPOSE 80/tcp
