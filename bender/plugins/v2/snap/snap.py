#!/usr/bin/python
# coding: utf-8

from .foscam import FoscamCamera
from bender.config import get_plugin_config, get_ssh_config
from bender.utils import check_port
from sshtunnel import SSHTunnelForwarder
import logging
import random
from bender.response import PictureResponse


COMMANDS = {
    'snap': {
        'short': 'Snap a pic',
        'description': 'Snap a picture from the home surveillance camera',
        'payload': 'SNAP',
    },
    # 'videosnap': {
    #     'description': 'Get a video of the last 30 seconds'
    # }
}

def __snap(cam):
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
    # os.remove(tmp_file)
    return PictureResponse('', tmp_file, repeat='SNAP')

def snap():
    cam_config = get_plugin_config(plugin='camera')

    if not check_port(cam_config['host'], cam_config['port']):
        logger = logging.getLogger(__name__)
        logger.info('Could not connect directly, connecting via SSH proxy')
        ssh_config = get_ssh_config(host=cam_config['proxy'])
        random_local_port = random.randint(1025, 65535)
        with SSHTunnelForwarder(
            (ssh_config['host'], ssh_config['port']),
            ssh_username=ssh_config['username'],
            ssh_password=ssh_config['password'],
            remote_bind_address=(cam_config['host'], cam_config['port']),
            local_bind_address=('127.0.0.1', random_local_port)
        ):
            logger.info(
                'SSH local forwarding: {}:{} -> {}:{} -> {}:{}'.format(
                    '127.0.0.1', random_local_port,
                    ssh_config['host'], ssh_config['port'],
                    cam_config['host'], cam_config['port']
                )
            )
            cam = FoscamCamera(
                '127.0.0.1',
                random_local_port,
                cam_config['username'],
                cam_config['password']
            )
            return __snap(cam)
    else:
        cam = FoscamCamera(
            cam_config['host'],
            cam_config['port'],
            cam_config['username'],
            cam_config['password']
        )
    return __snap(cam)
