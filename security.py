#!/usr/bin/python
# coding: utf-8

from config import get_authorized_users
import logging

def auth_required(f):
    '''
    Definition decorator for all functions required an authorized user
    Credit: http://stackoverflow.com/a/7590709
    '''
    def check_auth(bot, update, *args, **kwargs):
        '''
        Function to be applied on top of all decorated methods
        '''
        if not is_authorized(update):
            logger = logging.getLogger()
            logger.debug('NOT AUTHORIZED: ' + update.message.from_user.username)
            import bender
            return bender.send_message(bot, update, 'nope, nope. NOPE.')
        return f(bot, update, *args, **kwargs)
    return check_auth

def is_authorized(update):
    return update.message.from_user.username in get_authorized_users()
