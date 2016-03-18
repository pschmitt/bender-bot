#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from plugins.clear import clear
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

def emoji_test(bot, update):
    from telegram import Emoji
    chat_id = update.message.chat_id
    bot.sendMessage(chat_id=chat_id, text='{} Message sent!'.format(unicode(Emoji.HEAVY_CHECK_MARK, 'utf-8')))

if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    updater = telegram.Updater(token=config.get_token())
    bc.dispatcher = updater.dispatcher

    PLUGINS = [
        clear,
        gimme,
        insult,
        quote,
        random_fact,
        shell_exec,
        sms,
        snap,
    ]

    for p in PLUGINS:
        print(p)
        for c in p.COMMANDS:
            bc.dispatcher.addTelegramCommandHandler(c, getattr(p, c))

    # bc.dispatcher.addTelegramMessageHandler(emoji_test)
    bc.dispatcher.addTelegramMessageHandler(quote.quote)
    bc.dispatcher.addUnknownTelegramCommandHandler(unknown_command)
    bc.dispatcher.addErrorHandler(error_handler)

    # bc.dispatcher.addTelegramCommandHandler('help', help)
    # dispatcher.addTelegramCommandHandler('start', start)
    # dispatcher.addTelegramCommandHandler('insult', insult)
    # dispatcher.addTelegramCommandHandler('random', random_fact)
    # dispatcher.addTelegramCommandHandler('shell', shell_exec)
    # dispatcher.addTelegramCommandHandler('exec', shell_exec)
    # dispatcher.addTelegramCommandHandler('gimme', gimme)
    # dispatcher.addTelegramCommandHandler('lights', lights)
    # dispatcher.addTelegramCommandHandler('restart', restart)

    updater.start_polling()
    updater.idle()
