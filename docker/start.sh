#!/usr/bin/env ash

cd /app

[[ -r /app/requirements-runtime.txt ]] && pip install -r /app/requirements-runtime.txt

/usr/bin/gunicorn $PARAMS
