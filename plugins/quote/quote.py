#!/usr/bin/python
# coding: utf-8

from quotes import QUOTES
import random

COMMANDS = ['quote']

def quote(bot, update):
    from bender import send_message
    return send_message(bot, update, random.choice(QUOTES))
