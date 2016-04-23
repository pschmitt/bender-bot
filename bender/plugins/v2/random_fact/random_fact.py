#!/usr/bin/python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

COMMANDS = {
    'random_fact': {
        'short': 'Random fact',
        'description': 'Get a random fact',
        'aliases': ['random', 'rnd'],
        'payload': 'RANDOM_FACT'
    }
}

def random_fact():
    r = requests.get('http://randomfunfacts.com')
    s = BeautifulSoup(r.text, 'html.parser')
    return s.strong.i.text.strip()
