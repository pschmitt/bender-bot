#!/usr/bin/python
# coding: utf-8

from bot_controller import reset_message_handler

COMMANDS = {
    'cancel': {
        'description': 'Cancel current operation',
        'aliases': ['c']
    }
}

def cancel(bot, update):
    from bender import send_message
    if reset_message_handler():
        send_message(bot, update, 'Doks. I aborted the mission.')
    else:
        send_message(bot, update, 'I wasn\'t about to do shit. Anyfuck, I\'ve cancelled it')
