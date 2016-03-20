#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from security import auth_required
from telegram import Emoji
from utils import remove_first_word
from emoji import emoji

COMMANDS = {
    'gimme': {
        'description': 'Retrieve files',
        'aliases': ['get']
    }
}

@auth_required
def gimme(bot, update):
    from bender import send_message
    chat_id = update.message.chat_id
    text = remove_first_word(update.message.text)
    try:
        with open(text, 'rb') as f:
            return bot.sendDocument(chat_id=chat_id, document=f)
    except Exception as e:
        send_message(bot, update, '{} Shit hit the fan: {}'.format(emoji(Emoji.CROSS_MARK), e))
