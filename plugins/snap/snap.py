#!/usr/bin/python
# coding: utf-8

from .foscam import FoscamCamera
import os
import telegram
from security import auth_required
from config import get_config_section

COMMANDS = ['snap', 'videosnap']

@auth_required
def snap(bot, update):
    chat_id = update.message.chat_id
    cam_config = get_config_section(section='camera')
    cam = FoscamCamera(
        cam_config['host'],
        cam_config['port'],
        cam_config['username'],
        cam_config['password']
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
    bot.sendPhoto(chat_id=chat_id, photo=open(tmp_file, 'rb'))
    os.remove(tmp_file)

@auth_required
def videosnap(bot, update):
    raise telegram.error.TelegramError('This function is not implemented yet.')
