#!/bin/sh
set -e

# Substitute environment variables in nginx config
envsubst '${UPSTREAM_PORT}' < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf.tmp
mv /etc/nginx/nginx.conf.tmp /etc/nginx/nginx.conf

# Start nginx
exec "$@"