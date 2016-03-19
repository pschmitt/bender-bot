#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from emoji import emoji
from telegram import Emoji

COMMANDS = ['emojis']

def emojis(bot, update):
    from bender import send_message
    message = ''
    for e in [x for x in dir(Emoji) if x.isupper()]:
        message += '{}: {}\n'.format(emoji(getattr(Emoji, e)), e)
    send_message(bot, update, message)
