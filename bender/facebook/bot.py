#!/usr/bin/python
# coding: utf-8


from __future__ import print_function
import falcon
import json
import logging
import requests
import pprint
from shell import shell
from bender.utils import fuzzy_find_key
from bender.response import TextResponse, PictureResponse


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# Disable requests logs
# logging.getLogger('requests').setLevel(logging.WARNING)
# logging.getLogger('urllib3').setLevel(logging.WARNING)


class BenderBot():
    def __init__(self, verification_token, page_token, plugins=None):
        self.verification_token = verification_token
        self.page_token = page_token
        self.plugins = plugins
        self.FB_CHAT_API = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + self.page_token
        self.MAIN_MENU = []
        self.COMMAND_HANDLERS = {}
        self.CALLBACK_HANDLERS = {}
        self.HELP_TEXT = ''
        if plugins:
            for p in plugins:
                for c, value in p.COMMANDS.iteritems():
                    logging.info(c)
                    self.MAIN_MENU.append({
                        'type': 'postback',
                        'title': value['short'],
                        'payload': value['payload']
                    })
                    # cmd ist the actual function to be executed
                    cmd = getattr(p, c)

                    # Construct command handler dict
                    self.COMMAND_HANDLERS[c] = cmd
                    if 'aliases' in value:
                        for a in value['aliases']:
                            self.COMMAND_HANDLERS[a] = cmd

                    # Construct payload handler dict
                    if 'payload' in value:
                        self.CALLBACK_HANDLERS[value['payload']] = cmd

                    # Construct HELP command text
                    self.HELP_TEXT += '{} - {}'.format(c, value['description'])
                    if 'aliases' in value:
                        aliases = value['aliases']
                        self.HELP_TEXT += ' (Aliases: '
                        for a in aliases:
                            self.HELP_TEXT += a
                            # Close bracket if this is the last alias
                            if a == aliases[-1]:
                                self.HELP_TEXT += ')'
                            else:
                                self.HELP_TEXT += ', '
                    self.HELP_TEXT += '\r\n'
                    # Register 'help' to display HELP_TEXT
                    self.COMMAND_HANDLERS['help'] = lambda: self.HELP_TEXT
            # logger.debug(pprint.pformat(self.MAIN_MENU))
            # logger.debug(pprint.pformat(self.COMMAND_HANDLERS))
            # logger.debug(pprint.pformat(self.CALLBACK_HANDLERS))

    def send_message(self, recipient, message):
        if isinstance(message, PictureResponse):
            return self.send_picture(recipient, message)
        elif isinstance(message, TextResponse) or type(message) is str or type(message) is unicode:
            return self.send_text_message(recipient, message)

    def send_text_message(self, recipient, text):
        logger.debug('RESPONSE: {}'.format(text))
        # if text is a string, send it directly
        if type(text) in [str, unicode]:
            return requests.post(
                self.FB_CHAT_API,
                json={
                    'recipient': {'id': recipient},
                    'message': {'text': text},
                },
            )
        # Here we can safely assume that text is a TextResponse instance
        if not text.repeat:
            # No "repeat" button requested. Send the message
            return requests.post(
                self.FB_CHAT_API,
                json={
                    'recipient': {'id': recipient},
                    'message': {'text': text.text},
                },
            )
        # Repeat mode. Send answer as a button response
        return self.send_buttons(recipient, text.text, [{
            'type': 'postback',
            'title': 'Another!',
            'payload': text.repeat
        }])

    def send_buttons(self, recipient, title, buttons=None):
        return requests.post(
            self.FB_CHAT_API,
            json={
                'recipient': {'id': recipient},
                'message': {
                    'attachment': {
                        'type': 'template',
                        'payload': {
                            'template_type': 'button',
                            'text': title,
                            'buttons': buttons
                        }
                    }
                }
            }
        )

    def send_picture(self, recipient, picture):
        # curl
        # -F recipient='{"id":"USER_ID"}' \
        # -F message='{"attachment":{"type":"image", "payload":{}}}' \
        # -F filedata=@/tmp/testpng.png \
        # "https://graph.facebook.com/v2.6/me/messages?access_token=PAGE_ACCESS_TOKEN"

        cmd = 'curl -F recipient="{\'id\': \'' + str(recipient) + '\'}" ' \
            '-F message="{\'attachment\':{\'type\':\'image\', \'payload\':{}}}" ' \
            '-F filedata=@' + picture.picture + ' ' + self.FB_CHAT_API

        result = shell(cmd)
        logger.debug(result.output)
        if picture.repeat:
            self.send_buttons(recipient, ' ', [{
                'type': 'postback',
                'title': 'Another!',
                'payload': picture.repeat
            }])
        return result

        # # files = {'filedata': open(picture, 'rb')}
        # return requests.post(
        #     self.FB_CHAT_API,
        #     data={
        #         'recipient': {'id': recipient},
        #         'message': {
        #             'attachment': {
        #                 'type': 'image',
        #                 'payload': {}
        #             },
        #         },
        #         # 'filedata': {open(picture, 'rb')}
        #     },
        #     # files=files
        # )

    def main_menu(self, recipient):
        menu_parts = [self.MAIN_MENU[i:i+3] for i in range(0, len(self.MAIN_MENU), 3)] #zip(*[iter(self.MAIN_MENU)]*3)
        for part in menu_parts:
            logger.debug('PART# ' + str(part))
            # NOTE: Title cannot be empty, otherwise messenger wont show the
            # buttons
            self.send_buttons(recipient, 'Main menu' if part == menu_parts[0] else ' ', part)

    def handle_message(self, sender, text):
        k = fuzzy_find_key(self.COMMAND_HANDLERS, text)
        if k:
            response = self.COMMAND_HANDLERS[k]()
            return self.send_message(sender, response)
        return self.main_menu(sender)

    def handle_postback(self, sender, payload):
        if payload in self.CALLBACK_HANDLERS:
            response = self.CALLBACK_HANDLERS[payload]()
            return self.send_message(sender, response)
        return self.send_message(sender, 'Hu?')


class BenderResource:
    def __init__(self, verification_token, page_token, plugins=None):
        self.bot = BenderBot(verification_token, page_token, plugins)

    def on_get(self, req, resp):
        '''
        Handles GET requests
        '''
        # TODO Let the bot handle the requst
        if req.get_param('hub.verify_token') == self.bot.verification_token:
            resp.status = falcon.HTTP_200
            resp.body = req.get_param('hub.challenge', False)
        else:
            resp.status = falcon.HTTP_503
            resp.body = 'Wrong verification token'

    def on_post(self, req, resp):
        '''
        Handles POST requests
        '''
        try:
            raw_json = req.stream.read()
            result = json.loads(raw_json, encoding='utf-8')
        except ValueError:
                raise falcon.HTTPError(
                    falcon.HTTP_400,
                    'Malformed JSON',
                    'Could not decode the request body. The JSON was incorrect.'
                )
        except Exception as ex:
            raise falcon.HTTPError(
                falcon.HTTP_400,
                'Error',
                ex.message
            )
        # logger.debug(pprint.pformat(result))
        for msg in result['entry'][0]['messaging']:
            logger.debug(pprint.pformat(msg))
            sender_id = msg['sender']['id']
            if 'message' in msg and 'text' in msg['message']:
                text = msg['message']['text']
                logger.debug('# TEXT: ' + text)
                result = self.bot.handle_message(sender_id, text)
                if hasattr(result, 'json'):
                    logger.debug(result.json())
                else:
                    logger.debug(result)
            elif 'postback' in msg:
                payload = msg['postback']['payload']
                logger.debug('# POSTBACK PAYLOAD: ' + payload)
                result = self.bot.handle_postback(sender_id, payload)
                if hasattr(result, 'json'):
                    logger.debug(result.json())
                else:
                    logger.debug(result)
