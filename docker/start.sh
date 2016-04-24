#!/usr/bin/env ash

cd /app

/usr/bin/gunicorn $PARAMS
