#!/usr/bin/python
# encoding: utf-8

dispatcher = None
message_handler = None

def set_message_handler(handler):
    pass

def reset_message_handler(handler):
    dispatcher.addTelegramMessageHandler(msg_handler_recipient)
    dispatcher.removeTelegramMessageHandler(MESSAGE_HANDLER)

