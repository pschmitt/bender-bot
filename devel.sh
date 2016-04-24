#!/usr/bin/env bash

cd "$(dirname "$(readlink -f "$0")")"

# start dev server
nodemon --watch bender -e py --exec "python -m" bender.facebook

# let it fly
pagekite 8091 pschmitt.pagekite.me
