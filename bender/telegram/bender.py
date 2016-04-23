#!/usr/bin/python
# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from bender.telegram.register_commands import get_help_text
from bender.telegram.security import is_authorized
import telegram
import textwrap


def send_message(bot, update, text):
    chat_id = update.message.chat_id
    hide_kb = telegram.ReplyKeyboardHide()
    if len(text) > 3000: # The theoretical limit is 4096
        for chunk in textwrap.wrap(text, 3000):
            bot.sendMessage(chat_id=chat_id, text=chunk, reply_markup=hide_kb)
    else:
        bot.sendMessage(chat_id=chat_id, text=text, reply_markup=hide_kb)

def unknown_command(bot, update):
    send_message(bot, update, 'Hu!?')

def error_handler(bot, update, error):
    if is_authorized(update):
        err_msg = 'Update "{}" caused error "{}"'.format(update, error)
        send_message(bot, update, err_msg)

def help_cmd(bot, update):
    send_message(bot, update, get_help_text())
