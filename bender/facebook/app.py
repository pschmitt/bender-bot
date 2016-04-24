#!/usr/bin/env python
# coding: utf-8

import falcon
from .bot import BenderResource
from ..config import get_facebook_config


fb_conf = get_facebook_config()
endpoint = fb_conf.get('endpoint', '/')

# falcon.API instances are callable WSGI apps
app = falcon.API()


from bender.plugins.v2.insult import insult
from bender.plugins.v2.random_fact import random_fact
from bender.plugins.v2.quote import quote
from bender.plugins.v2.snap import snap
# from bender.plugins.v2.lights import lights

PLUGINS = [
    # 'bender.plugins.v2.insult',
    # 'bender.plugins.v2.quote',
    # 'bender.plugins.v2.random_fact'
    insult,
    quote,
    random_fact,
    snap,
    # lights
]

# Resources are represented by long-lived class instances
main = BenderResource(
    fb_conf['verification_token'], fb_conf['page_token'], PLUGINS
)

app.add_route(endpoint, main)
