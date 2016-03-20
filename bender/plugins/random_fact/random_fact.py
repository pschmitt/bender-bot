#!/usr/bin/python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

COMMANDS = {
    'random_fact': {
        'description': 'Get a random fact',
        'aliases': ['random', 'rnd']
    }
}

def __random():
    r = requests.get('http://randomfunfacts.com')
    s = BeautifulSoup(r.text)
    return s.strong.i.text.strip()

def random_fact(bot, update):
    from bender import send_message
    send_message(bot, update, text=__random())
