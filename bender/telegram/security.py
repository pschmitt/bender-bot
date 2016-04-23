#!/usr/bin/python
# coding: utf-8

import logging

def auth_required(f):
    '''
    Definition decorator for all functions requiring an authorized user
    Credit: http://stackoverflow.com/a/7590709
    '''
    def check_auth(bot, update, *args, **kwargs):
        '''
        Function to be applied on top of all decorated methods
        '''
        if not is_authorized(update):
            logger = logging.getLogger()
            logger.debug('NOT AUTHORIZED: ' + update.message.from_user.username)
            from bender.telegram.bender import send_message
            return send_message(bot, update, 'nope, nope. NOPE.')
        return f(bot, update, *args, **kwargs)
    return check_auth

def is_authorized(update):
    from bender.telegram.config import get_authorized_users
    return update.message.from_user.username in get_authorized_users()
