#!/usr/bin/python
# coding: utf-8

from __future__ import print_function
import argparse
from bender.config import get_facebook_config, get_contacts
from bot import BenderBot


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('RECIPIENT', help='Recipient of the message')
    parser.add_argument('MESSAGE', help='Message text')
    args = parser.parse_args()

    # config
    fb_conf = get_facebook_config()
    contacts = get_contacts()

    bot = BenderBot(fb_conf['verification_token'], fb_conf['page_token'])

    recipient = args.RECIPIENT

    # Get facebook id fron contacts if the given value is not an integer ID
    if not recipient.isdigit():
        for k, v in contacts.iteritems():
            # Check if the key "contact name" corresponds
            if k.lower() == args.RECIPIENT.lower():
                recipient = str(contacts[k]['facebook']['id'])
                break
            else:
                # Search in the nicknames section
                for n in v['nicknames']:
                    if n.lower() == args.RECIPIENT.lower():
                        recipient = str(contacts[k]['facebook']['id'])
                        break

    assert recipient.isdigit(), 'Recipient ID must be an integer ' + recipient

    # print(bot.send_message(recipient, args.MESSAGE).json())
    print(recipient)
    from bender.plugins.v2.snap.snap import snap
    pic = snap()
    print(bot.send_picture(recipient, title=args.MESSAGE, picture=pic.picture).output())

