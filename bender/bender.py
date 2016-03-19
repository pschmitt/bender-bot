#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from plugins.clear import clear
from plugins.emojis import emojis
from plugins.lights import lights
from plugins.quote import quote
from plugins.shell_exec import shell_exec
from plugins.sms import sms
from plugins.snap import snap
from plugins.random_fact import random_fact
from plugins.insult import insult
from plugins.gimme import gimme
from security import is_authorized
import config
import logging
import telegram
import textwrap
import bot_controller as bc

logger = logging.getLogger(__name__)

def send_message(bot, update, text):
    chat_id = update.message.chat_id
    hide_kb = telegram.ReplyKeyboardHide()
    # logger.debug(text)
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

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    updater = telegram.Updater(token=config.get_token())
    bc.dispatcher = updater.dispatcher

    PLUGINS = [
        clear,
        emojis,
        gimme,
        insult,
        lights,
        quote,
        random_fact,
        shell_exec,
        sms,
        snap,
    ]
    HELP = ''

    for p in PLUGINS:
        for c in p.COMMANDS:
            cmd = getattr(p, c)
            bc.dispatcher.addTelegramCommandHandler(c, cmd)
            # Set up command aliases
            if hasattr(p, 'ALIASES'):
                if c in p.ALIASES:
                    for alias in p.ALIASES[c]:
                        bc.dispatcher.addTelegramCommandHandler(alias, cmd)

    bc.dispatcher.addTelegramMessageHandler(quote.quote)
    bc.dispatcher.addUnknownTelegramCommandHandler(unknown_command)
    bc.dispatcher.addErrorHandler(error_handler)
    # bc.dispatcher.addTelegramCommandHandler('help', help)

    updater.start_polling()
    updater.idle()
