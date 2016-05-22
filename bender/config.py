#!/usr/bin/python
# coding: utf-8

import yaml
import logging

logger = logging.getLogger(__name__)


def get_config(config_file='bender.yaml'):
    with open(config_file) as f:
        config = yaml.load(f)
    return config

def get_config_section(config_file='bender.yaml', section='bot'):
    return get_config(config_file)[section]

def get_bot_config(config_file='bender.yaml', backend='telegram'):
    return get_config_section(config_file, section='bot')[backend]

def get_plugin_config(config_file='bender.yaml', plugin=None):
    c = get_config_section(config_file, 'plugins')
    return c[plugin] if plugin else c

def get_contacts(config_file='bender.yaml'):
    return get_config_section(config_file, section='contacts')

def get_ssh_config(config_file='bender.yaml', host=None):
    c = get_config_section(config_file, section='ssh')
    return c[host] if host else c

# Telegram config
def get_telegram_config(config_file='bender.yaml'):
    return get_bot_config(config_file, 'telegram')

def get_telegram_token(config_file='bender.yaml'):
    return get_telegram_config(config_file)['token']

def get_telegram_authorized_users(config_file='bender.yaml'):
    return get_telegram_config(config_file)['authorized_users']

# Facebook config
def get_facebook_config(config_file='bender.yaml'):
    return get_bot_config(config_file, 'facebook')

def get_facebook_page_token(config_file='bender.yaml'):
    return get_facebook_config(config_file)['page_token']

def get_facebook_verification_token(config_file='bender.yaml'):
    return get_facebook_config(config_file)['verification_token']

def get_facebook_authorized_users(config_file='bender.yaml'):
    return [
        unicode(u) for u in \
        get_facebook_config(config_file)['authorized_users']
    ]

def get_facebook_admins(config_file='bender.yaml'):
    try:
        return [
            unicode(u) for u in \
            get_facebook_config(config_file)['administrators']
        ]
    except KeyError:
        logger.warning('No administrator defined')

