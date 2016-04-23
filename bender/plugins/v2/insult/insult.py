#!/usr/bin/python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

COMMANDS = {
    'insult': {
        'short': 'Insult me',
        'description': 'Get insulted, for free!',
        'payload': 'INSULT',
    }
}

def insult():
    r = requests.get('http://www.insultgenerator.org/')
    s = BeautifulSoup(r.text, 'html.parser')
    return s.br.text.strip()
