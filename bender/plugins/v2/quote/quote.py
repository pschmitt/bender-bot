#!/usr/bin/python
# coding: utf-8

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

def quote():
    return random.choice(QUOTES)
