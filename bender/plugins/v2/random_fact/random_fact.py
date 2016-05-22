#!/usr/bin/python
# coding: utf-8

from bender.response import TextResponse
from bs4 import BeautifulSoup
import requests

COMMANDS = {
    'random_fact': {
        'short': 'Random fact',
        'description': 'Get a random fact',
        'aliases': ['random', 'rnd'],
        'payload': 'RANDOM_FACT'
    }
}

def random_fact(sender):
    r = requests.get('http://randomfunfacts.com')
    s = BeautifulSoup(r.text, 'html.parser')
    text = s.strong.i.text.strip()
    return TextResponse(
        text, repeat=COMMANDS['random_fact']['payload']
    )
