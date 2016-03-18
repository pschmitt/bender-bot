#!/usr/bin/python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

COMMANDS = ['insult']

def __insult():
    r = requests.get('http://www.insultgenerator.org/')
    s = BeautifulSoup(r.text)
    return s.br.text.strip()

def insult(bot, update):
    from bender import send_message
    send_message(bot, update, text=__insult())
