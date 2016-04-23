#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from telegram import Emoji
from bender.telegram.emoji import emoji
from bender.telegram.security import auth_required
from bender.utils import remove_first_word

COMMANDS = {
    'gimme': {
        'description': 'Retrieve files',
        'aliases': ['get']
    }
}

@auth_required
def gimme(bot, update):
    from bender.telegram.bender import send_message
    chat_id = update.message.chat_id
    text = remove_first_word(update.message.text)
    try:
        with open(text, 'rb') as f:
            return bot.sendDocument(chat_id=chat_id, document=f)
    except Exception as e:
        send_message(bot, update, '{} Shit hit the fan: {}'.format(emoji(Emoji.CROSS_MARK), e))
