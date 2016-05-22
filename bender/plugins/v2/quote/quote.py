#!/usr/bin/python
# coding: utf-8

from bender.response import TextResponse
from quotes import QUOTES
import random

COMMANDS = {
    'quote': {
        'short': 'Bender quotes',
        'description': 'Get quotes from Bender Bending Rodriguez',
        'payload': 'QUOTE',
        'aliases': ['futurama', 'bender']
    }
}

def quote(sender):
    text = random.choice(QUOTES)
    return TextResponse(
        text, repeat=COMMANDS['quote']['payload']
    )
