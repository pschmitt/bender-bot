#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from telegram import Emoji

COMMANDS = {
    'emoji': {
        'description': 'Show all emojis telegram supports'
    },
}

def emoji(e):
    if hasattr(Emoji, e):
        return unicode(getattr(Emoji, e), ('utf-8'))
    return unicode(e, ('utf-8'))
