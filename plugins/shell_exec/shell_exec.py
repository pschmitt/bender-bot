#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from security import auth_required
from utils import remove_first_word
from telegram import Emoji
from emoji import emoji
from shell import shell as sh

COMMANDS = ['shell_exec']

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
def shell_exec(bot, update):
    from bender import send_message
    # Remove first word (shell or /shell)
    text = remove_first_word(update.message.text)
    response = __shell(text)
    send_message(bot, update, response)
