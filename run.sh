#!/usr/bin/env sh

cd "$(dirname "$(readlink -f "$0")")/bender"

source ~/.local/share/virtualenvs/bender-bot/bin/activate

python bender.py
