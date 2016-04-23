#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from bender.telegram.security import auth_required
from bender.telegram.emoji import emoji
from shell import shell as sh
from telegram import Emoji
from bender.utils import remove_first_word
import bender.telegram.bot_controller as bot_controller

COMMANDS = {
    'shell_exec': {
        'description': 'Execute a shell command',
        'aliases': ['shell', 'sh']
    },
    'ping': {
        'description': 'Ping a host'
    },
    'ls': {
        'description': 'List files in folder'
    },
    'nmap': {
        'description': 'Network scan'
    }
}

def __shell(cmd):
    try:
        s = sh(cmd)
        errors = s.errors(raw=True)
        if errors:
            response = u'{} FAIL: {}'.format(emoji(Emoji.PILE_OF_POO), errors)
        else:
            response = s.output(raw=True)
    except OSError as e:
        response = '{} That did\'t go well: {}'.format(emoji(Emoji.CROSS_MARK), e)
    return response

def __shell_exec(bot, update, command, text):
    from bender import send_message
    p = __shell('{} {}'.format(command, text))
    send_message(bot, update, p)

@auth_required
def message_handler_command(bot, update):
    from bender import send_message
    text = update.message.text
    if text:
        response = __shell(text)
    else:
        response = 'Whatever'
    bot_controller.reset_message_handler()
    send_message(bot, update, response)

@auth_required
def shell_exec(bot, update):
    from bender import send_message
    # Remove first word (shell or /shell)
    text = remove_first_word(update.message.text)
    if text:
        response = __shell(text)
    else:
        response = 'What command should I run?'
        bot_controller.set_message_handler(message_handler_command)
    send_message(bot, update, response)

@auth_required
def ping(bot, update):
    from bender import send_message
    text = remove_first_word(update.message.text.strip())
    if not text:
        send_message(bot, update, 'Missing host')
    else:
        p = __shell('ping -c 1 -w 1 {}'.format(text))
        send_message(bot, update, p)

@auth_required
def ls(bot, update):
    text = remove_first_word(update.message.text.strip())
    __shell_exec(bot, update, 'ls -al', text)

@auth_required
def nmap(bot, update):
    text = remove_first_word(update.message.text.strip())
    __shell_exec(bot, update, 'nmap', text)
