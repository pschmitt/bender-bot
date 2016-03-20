#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from security import auth_required
from utils import remove_first_word
from telegram import Emoji
from emoji import emoji
from shell import shell as sh
import bot_controller

COMMANDS = ['shell_exec', 'ping', 'ls']
ALIASES = {'shell_exec': ['shell', 'sh']}

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
    from bender import send_message
    text = remove_first_word(update.message.text.strip())
    p = __shell('ls -al {}'.format(text))
    send_message(bot, update, p)
