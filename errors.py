#!/usr/bin/python
# coding: utf-8

from bender import send_message

def not_implemented(bot, update):
    message = 'Nah. This ain\'t implemented yet.'
    send_message(bot, update, message)
