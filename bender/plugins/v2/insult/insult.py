#!/usr/bin/python
# coding: utf-8

from bender.response import TextResponse
from bs4 import BeautifulSoup
import requests

COMMANDS = {
    'insult': {
        'short': 'Insult me',
        'description': 'Get insulted, for free!',
        'payload': 'INSULT',
    }
}

def insult(sender):
    r = requests.get('http://www.insultgenerator.org/')
    s = BeautifulSoup(r.text, 'html.parser')
    text = s.br.text.strip()
    return TextResponse(
        text, repeat=COMMANDS['insult']['payload']
    )
