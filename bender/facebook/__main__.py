#!/usr/bin/env python
# coding: utf-8

from ..config import get_facebook_config
from app import app
import bjoern
import logging


if __name__ == '__main__':
    fb_conf = get_facebook_config()
    address = fb_conf.get('bind_address', '127.0.0.1')
    port = int(fb_conf.get('bind_port', 8091))
    endpoint = fb_conf.get('endpoint', '/')

    logger = logging.getLogger(__name__)
    logger.debug('Start on {}:{}{}'.format(address, port, endpoint))

    bjoern.run(
        app,
        address,
        port
    )
