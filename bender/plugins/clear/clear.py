#!/usr/bin/python
# coding: utf-8

COMMANDS = {
    'clear': {
        'description': 'Clear the screen'
    }
}

def clear(bot, update):
    from bender import send_message
    message = '''
    .























































































    .
    '''
    send_message(bot, update, message)
