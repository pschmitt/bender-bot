#!/usr/bin/python
# coding: utf-8

import logging
import bender.config as config

logger = logging.getLogger()


def auth_required(f):
    '''
    Definition decorator for all functions requiring an authorized user
    Credit: http://stackoverflow.com/a/7590709
    '''
    def check_auth(sender, *args, **kwargs):
        '''
        Function to be applied on top of all decorated methods
        '''
        if not is_authorized(sender):
            logger.debug('NOT AUTHORIZED: ' + sender)
            return 'nope, nope. NOPE.'
        return f(sender, *args, **kwargs)
    return check_auth

def is_authorized(sender):
    logger.info(
        'Check sender {} {}'.format(config.get_facebook_authorized_users(), type(sender))
    )
    return sender in config.get_facebook_authorized_users()
