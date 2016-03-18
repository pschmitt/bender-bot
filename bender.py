#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
# from __future__ import unicode_literals
from bs4 import BeautifulSoup
from foscam_python_lib.foscam import FoscamCamera
from phue import Bridge
from quotes import QUOTES
from shell import shell
from telegram import Updater, Emoji
import gammu.smsd
import logging
import os
import phonenumbers
import random
import requests
import sys
import telegram
import textwrap
import yaml

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# from os.path import getmtime
# WATCHED_FILES = [__file__]
# WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]
# while True:
#     for f, mtime in WATCHED_FILES_MTIMES:
#         if getmtime(f) != mtime:
#             os.execv(__file__, sys.argv)

with open('bender.yaml', 'r') as f:
    config = yaml.load(f)
AUTHORIZED_USERS = config['bot']['authorized_users']
TOKEN = config['bot']['token']

MODE = {}
MODE_SMS_RECIPIENT = 'sms_recipient'
MODE_SMS_TEXT = 'sms_text'
MODE_SHELL = 'shell'
MODE_LIGHTS = 'lights'
SMS_RECIPIENT = 'recipient'

def remove_first_word(string):
    return ' '.join(string.split()[1:])

def first_word(string):
    return string.partition(' ')[0]

def __quote():
    return random.choice(QUOTES)

def __insult():
    r = requests.get('http://www.insultgenerator.org/')
    s = BeautifulSoup(r.text)
    return s.br.text.strip()

def __random_fact():
    r = requests.get('http://randomfunfacts.com')
    s = BeautifulSoup(r.text)
    return s.strong.i.text.strip()

def __shell(cmd):
    try:
        sh = shell(cmd)
        errors = sh.errors(raw=True)
        if errors:
            # http://apps.timwhitlock.info/emoji/tables/unicode
            response = u'{} FAIL: {}'.format(Emoji.PILE_OF_POO, errors)
        else:
            response = sh.output(raw=True)
    except OSError as e:
        response = 'That did\'t go well: {}'.format(e)
    return response

def __gammu_sms(recipient, text):
    smsd = gammu.smsd.SMSD('/etc/gammu-smsdrc')
    message = {'Text': text, 'SMSC': {'Location': 1}, 'Number': recipient}
    return smsd.InjectSMS([message])

def __valid_phone_number(number):
    try:
        phonenumbers.parse(number, 'FR')
        return True
    except phonenumbers.NumberParseException:
        return False

def __sms(text):
    try:
        fw = first_word(text)
        if __valid_phone_number(fw):
            recipient = first_word
            text = remove_first_word(text)
        else:
            recipient = '+33671326033'
        return __gammu_sms(recipient, text)
    except Exception as e:
        return 'That did\'t go well: {}'.format(e)

def __bridge():
    return Bridge(ip=config['hue']['host'], username=config['hue']['username'])

def __get_light_by_name(bridge, name):
    for l in bridge.lights:
        # logger.debug(type(name))
        # logger.debug('VS')
        # logger.debug(type(l.name))
        if l.name == name.encode('utf-8'):
            logger.debug('#### MATCH')
            return l

def __light_toggle(light):
    b = __bridge()
    l = __get_light_by_name(b, light)
    b.set_light(l.light_id, 'on', not l.on)

def __help():
    return '''
    Available commands:
    /shell COMMAND
    /insult
    /quote
    /random
    /sms [NUMBER] MESSAGE
    '''

def send_message(bot, update, text):
    chat_id = update.message.chat_id
    hide_kb = telegram.ReplyKeyboardHide()
    # logger.debug(text)
    if len(text) > 3000: # The theoretical limit is 4096
        for chunk in textwrap.wrap(text, 3000):
            bot.sendMessage(chat_id=chat_id, text=chunk, reply_markup=hide_kb)
    else:
        bot.sendMessage(chat_id=chat_id, text=text, reply_markup=hide_kb)

def error(bot, update, error):
    err_msg = 'Update "{}" caused error "{}"'.format(update, error)
    logger.warn(err_msg)
    if update.message.from_user.username in AUTHORIZED_USERS:
        bot.sendMessage(chat_id=update.message.chat_id, text=err_msg)

def help(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=__help())

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text='010101001')

def echo(bot, update):
    global SMS_RECIPIENT
    chat_id = update.message.chat_id
    text = update.message.text
    ltext = update.message.text.lower()
    if chat_id in MODE:
        if MODE[chat_id] == MODE_SMS_RECIPIENT:
            logger.debug('SEND MESSAGE TO ' + ltext)
            if ltext == 'me':
                SMS_RECIPIENT = '+33671326033'
                logger.debug('SEND MESSAGE TO ' + SMS_RECIPIENT)
            elif ltext == 'marine':
                SMS_RECIPIENT = '+33625432291'
            else:
                fw = first_word(ltext)
                if __valid_phone_number(fw):
                    SMS_RECIPIENT = fw
                else:
                    del MODE[chat_id]
                    return send_message(bot, update, 'This is not a valid phone number')
            MODE[chat_id] = MODE_SMS_TEXT
            return send_message(
                bot, update,
                'Okay and what should I tell {} ({})'.format(ltext, SMS_RECIPIENT)
            )
        elif MODE[chat_id] == MODE_SMS_TEXT:
            del MODE[chat_id]
            logger.debug('Send SMS to ' + SMS_RECIPIENT)
            return send_message(
                bot, update,
                __gammu_sms(SMS_RECIPIENT, ltext)
            )
        elif MODE[chat_id] == MODE_LIGHTS:
            del MODE[chat_id]
            __light_toggle(text)
            response = u'Toggled light {}'.format(text)
            return send_message(bot, update, response)
        else:
            del MODE[chat_id]
            return send_message(bot, update, 'Something went wrong here')
    if update.message.from_user.username in AUTHORIZED_USERS:
        if ltext.startswith('shell'):
            response = __shell(remove_first_word(update.message.text))
        elif ltext.startswith('sms'):
            response = __sms(remove_first_word(update.message.text))
        else:
            response = text_response(ltext)
    else:
        response = text_response(ltext)
    send_message(bot, update, response)

def text_response(text):
    if text == 'random':
        response = __random_fact()
    elif text == 'insult':
        response = __insult()
    elif text == 'help':
        response = __help()
    elif text == 'ta gueule' or text == 'tg':
        response = 'Ta gueule.'
    elif text == 'fuck you':
        response = 'Well fuck you too'
    else:
        response = __quote()
    return response

def unknown(bot, update):
    send_message(bot, update, text='Hu!?')

def quote(bot, update):
    send_message(bot, update, text=__quote())

def insult(bot, update):
    send_message(bot, update, text=__insult())

def random_fact(bot, update):
    send_message(bot, update, text=__random_fact())

def shell_exec(bot, update):
    # Remove first word (shell or /shell)
    text = remove_first_word(update.message.text)
    if update.message.from_user.username in AUTHORIZED_USERS:
        response = __shell(text)
    else:
        response = 'NOPE'
    # bot.sendMessage(chat_id=update.message.chat_id, text=response)
    send_message(bot, update, response)

def sms(bot, update):
    chat_id = update.message.chat_id
    text = remove_first_word(update.message.text).strip()
    if update.message.from_user.username in AUTHORIZED_USERS:
        if not text:
            # response = 'Who do you want to message?'
            custom_keyboard = [[ 'Marine', 'Me' ]]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            MODE[chat_id] = MODE_SMS_RECIPIENT
            return bot.sendMessage(chat_id=chat_id, text='Which light do you want me toggle?', reply_markup=reply_markup)
        else:
            response = __sms(text)
    else:
        response = 'NOPE'
    bot.sendMessage(chat_id=update.message.chat_id, text=response)

def snap(bot, update):
    if update.message.from_user.username in AUTHORIZED_USERS:
        chat_id = update.message.chat_id
        cam = FoscamCamera(
            config['camera']['host'],
            config['camera']['port'],
            config['camera']['username'],
            config['camera']['password']
        )
        # import tempfile
        # tmp_file = tempfile.NamedTemporaryFile()
        # try:
        #     pic = cam.snap_picture_2()[1]
        #     tmp_file.write(pic)
        #     bot.sendPhoto(chat_id=chat_id, photo=tmp_file)
        # finally:
        #     tmp_file.close()
        tmp_file = '/tmp/.snap.jpg'
        pic = cam.snap_picture_2()[1]
        with open(tmp_file, 'wb') as f:
            f.write(pic)
        logger.debug('MESSAGE')
        logger.debug(update)
        bot.sendPhoto(chat_id=chat_id, photo=open(tmp_file, 'rb'))
        os.remove(tmp_file)
    else:
        return send_message(bot, update, 'NOPE')

def gimme(bot, update):
    if update.message.from_user.username in AUTHORIZED_USERS:
        chat_id = update.message.chat_id
        text = remove_first_word(update.message.text)
        try:
            with open(text, 'rb') as f:
                return bot.sendDocument(chat_id=chat_id, document=f)
        except Exception as e:
            send_message(bot, update, '{} Shit hit the fan: {}'.format(Emoji.POODLE, e))
    else:
        return send_message(bot, update, 'NOPE')

def lights(bot, update):
    chat_id = update.message.chat_id
    text = remove_first_word(update.message.text)
    if update.message.from_user.username in AUTHORIZED_USERS:
        b = __bridge()
        light_names = [x.name for x in b.lights]
        # response = '\n'.join(light_names)
        if not text:
            custom_keyboard = [light_names]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            MODE[chat_id] = MODE_LIGHTS
            return bot.sendMessage(chat_id=chat_id, text='Who should I message?', reply_markup=reply_markup)
    else:
        send_message(bot, update, 'NOPE')

def restart(bot, update):
    logger.debug('file: {}'.format(__file__))
    os.execv(
        '/home/pschmitt/.local/share/virtualenvs/bender-bot/bin/python {}'.format(__file__),
        sys.argv
    )

if __name__ == '__main__':
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.addTelegramCommandHandler('help', help)
    dispatcher.addTelegramCommandHandler('start', start)
    dispatcher.addTelegramCommandHandler('insult', insult)
    dispatcher.addTelegramCommandHandler('random', random_fact)
    dispatcher.addTelegramCommandHandler('shell', shell_exec)
    dispatcher.addTelegramCommandHandler('exec', shell_exec)
    dispatcher.addTelegramCommandHandler('quote', quote)
    dispatcher.addTelegramCommandHandler('sms', sms)
    dispatcher.addTelegramCommandHandler('snap', snap)
    dispatcher.addTelegramCommandHandler('gimme', gimme)
    dispatcher.addTelegramCommandHandler('lights', lights)
    dispatcher.addTelegramCommandHandler('restart', restart)
    dispatcher.addTelegramMessageHandler(echo)
    dispatcher.addUnknownTelegramCommandHandler(unknown)
    dispatcher.addErrorHandler(error)

    updater.start_polling()
    updater.idle()
