#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from config import get_config_section
from phue import Bridge
from utils import remove_first_word
from telegram import ReplyKeyboardMarkup
from telegram import Emoji
from emoji import emoji
import bot_controller
import re

COMMANDS = ['lights']

class LightNotFoundException(Exception):
    pass

def __bridge():
    config = get_config_section(section='hue')
    return Bridge(ip=config['host'], username=config['username'])

def __get_light_by_name(bridge, name):
    for l in bridge.lights:
        if l.name == name.encode('utf-8'):
            return l
    raise LightNotFoundException()

def __light_toggle(light):
    b = __bridge()
    l = __get_light_by_name(b, light)
    b.set_light(l.light_id, 'on', not l.on)
    return l.on

def message_handler_light_selection(bot, update):
    from bender import send_message
    text = re.sub(r': (on|off)', '', update.message.text)
    try:
        state = __light_toggle(text)
        response = u'{} Toggled light {} (state: {})'.format(emoji(Emoji.HEAVY_CHECK_MARK), text, 'on' if state else 'off')
    except LightNotFoundException:
        response = u'{} Could not find light named {}'.format(emoji(Emoji.CROSS_MARK), text)
    return send_message(bot, update, response)

def lights(bot, update):
    chat_id = update.message.chat_id
    text = remove_first_word(update.message.text)
    b = __bridge()
    light_names = ['{}: {}'.format(unicode(x.name, 'utf-8'), 'on' if x.on else 'off') for x in b.lights]
    if not text:
        custom_keyboard = [light_names]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        bot.sendMessage(chat_id=chat_id, text='What lamp should I toggle?', reply_markup=reply_markup)
        bot_controller.set_message_handler(message_handler_light_selection)

