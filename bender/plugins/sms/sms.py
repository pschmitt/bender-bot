#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from config import get_config_section
from emoji import emoji
from security import auth_required
from telegram import Emoji
import bot_controller
import gammu.smsd
import logging
import phonenumbers
import telegram
import utils

COMMANDS = ['sms']
CONTACTS = get_config_section(section='contacts')
DEFAULT_LOCATION = 'FR'

RECIPIENT = None

logger = logging.getLogger(__name__)

def __valid_phone_number(number):
    try:
        phonenumbers.parse(number, DEFAULT_LOCATION)
        return True
    except phonenumbers.NumberParseException:
        return False

def __gammu_sms(recipient, text):
    smsd = gammu.smsd.SMSD('/etc/gammu-smsdrc')
    message = {'Text': text, 'SMSC': {'Location': 1}, 'Number': recipient}
    return smsd.InjectSMS([message])

@auth_required
def msg_handler_content(bot, update):
    global RECIPIENT
    chat_id = update.message.chat_id
    bot_controller.reset_message_handler()
    bot.sendMessage(
        chat_id=chat_id,
        text='{} Message sent!'.format(emoji(Emoji.WHITE_HEAVY_CHECK_MARK))
    )

@auth_required
def msg_handler_recipient(bot, update):
    global RECIPIENT
    chat_id = update.message.chat_id
    text = update.message.text
    if text in CONTACTS:
        RECIPIENT = CONTACTS[text]
    else:
        if __valid_phone_number(text):
            RECIPIENT = text
        else:
            RECIPIENT = 'NONUMBER'
    hide_kb = telegram.ReplyKeyboardHide()
    bot.sendMessage(chat_id=chat_id, text='What do I send {}?'.format(RECIPIENT), reply_markup=hide_kb)
    bot_controller.set_message_handler(msg_handler_content)

@auth_required
def sms(bot, update):
    chat_id = update.message.chat_id
    text = utils.remove_first_word(update.message.text).strip()
    if not text:
        custom_keyboard = [CONTACTS.keys()]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        logger.debug(bot_controller.dispatcher)
        bot.sendMessage(chat_id=chat_id, text='Who do you want to message?', reply_markup=reply_markup)
        logger.debug(bot_controller.dispatcher.telegram_message_handlers)
        bot_controller.set_message_handler(msg_handler_recipient)

