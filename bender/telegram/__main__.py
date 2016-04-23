#!/usr/bin/env python
# coding: utf-8


from __future__ import absolute_import
from bender.plugins.cancel import cancel
from bender.plugins.clear import clear
from bender.plugins.emojis import emojis
from bender.plugins.lights import lights
from bender.plugins.quote import quote
from bender.plugins.shell_exec import shell_exec
from bender.plugins.sms import sms
from bender.plugins.snap import snap
from bender.plugins.random_fact import random_fact
from bender.plugins.insult import insult
from bender.plugins.gimme import gimme
from bender.telegram.bender import error_handler, unknown_command, help_cmd
from bender.telegram import bot_controller as bc
from telegram import Updater
from bender.config import get_telegram_token
import logging


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    updater = Updater(token=get_telegram_token())
    bc.dispatcher = updater.dispatcher

    PLUGINS = [
        cancel,
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
    for p in PLUGINS:
        for c, value in p.COMMANDS.iteritems():
            cmd = getattr(p, c)
            bc.dispatcher.addTelegramCommandHandler(c, cmd)
            if 'aliases' in value:
                for alias in value['aliases']:
                    bc.dispatcher.addTelegramCommandHandler(alias, cmd)

    bc.dispatcher.addTelegramMessageHandler(quote.quote)
    bc.dispatcher.addUnknownTelegramCommandHandler(unknown_command)
    bc.dispatcher.addErrorHandler(error_handler)
    bc.dispatcher.addTelegramCommandHandler('help', help_cmd)

    updater.start_polling()
    updater.idle()
