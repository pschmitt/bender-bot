#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
from bender.config import get_plugin_config, get_ssh_config
from bender.facebook.security import auth_required
from bender.utils import check_port
from bender.utils import random_local_port
from phue import Bridge
from sshtunnel import SSHTunnelForwarder
import logging

logger = logging.getLogger()

COMMANDS = {
    'lights': {
        'short': 'Toggle lights',
        'description': 'Toggle a light',
        'payload': 'LIGHTS'
    }
}

class LightNotFoundException(Exception):
    pass

def __bridge():
    hue_config = get_plugin_config(plugin='hue')
    if not check_port(hue_config['host'], hue_config['port']):
        ssh_config = get_ssh_config(host=hue_config['proxy'])
        random_port = random_local_port()
        with SSHTunnelForwarder(
            (ssh_config['host'], ssh_config['port']),
            ssh_username=ssh_config['username'],
            ssh_password=ssh_config['password'],
            remote_bind_address=(hue_config['host'], hue_config['port']),
            local_bind_address=('127.0.0.1', random_port)
        ):
            logger.info(
                'SSH local forwarding: {}:{} -> {}:{} -> {}:{}'.format(
                    '127.0.0.1', random_port,
                    ssh_config['host'], ssh_config['port'],
                    hue_config['host'], hue_config['port']
                )
            )
            b = Bridge(ip='{}:{}'.format('127.0.0.1', random_port), username=hue_config['username'])
            # return [u'{}: {}'.format(unicode(x.name, 'utf-8'), '💡' if x.on else 'off') for x in b.lights]
            return [
                '{}: {}'.format(
                    unicode(x.name, 'utf-8'), ':bulb:' if x.on else ':new_moon:'
                ) for x in b.lights
            ]
            # return ['{}: {}'.format(unicode(x.name, 'utf-8'), ':bulb:' if x.on else 'off') for x in b.lights]
    return Bridge(ip='{}:{}'.format(hue_config['host'], hue_config.get('port', 80)), username=hue_config['username'])

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
    # text = re.sub(r': (on|off)', '', update.message.text)
    # try:
    #     state = __light_toggle(text)
    #     response = u'{} Toggled light {} (state: {})'.format(emoji(Emoji.WHITE_HEAVY_CHECK_MARK), text, 'on' if state else 'off')
    # except LightNotFoundException:
    #     response = u'{} Could not find light named {}'.format(emoji(Emoji.CROSS_MARK), text)
    pass

@auth_required
def lights(sender):
    b = __bridge()
    logger.debug(b)
    return b
    # logger = logging.getLogger(__name__)
    # logger.debug('## LIGHTS')
    # logger.debug(b.lights)
    # return ['{}: {}'.format(unicode(x.name, 'utf-8'), 'on' if x.on else 'off') for x in b.lights]
