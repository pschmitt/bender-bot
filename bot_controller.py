#!/usr/bin/python
# encoding: utf-8

dispatcher = None
ORIGINAL_MESSAGE_HANDLERS = None

def __remove_all_message_handlers():
    for h in dispatcher.telegram_message_handlers:
        dispatcher.removeTelegramMessageHandler(h)

def set_message_handler(handler):
    global ORIGINAL_MESSAGE_HANDLERS
    ORIGINAL_MESSAGE_HANDLERS = dispatcher.telegram_message_handlers
    __remove_all_message_handlers()
    dispatcher.addTelegramMessageHandler(handler)

def reset_message_handler():
    __remove_all_message_handlers()
    for h in ORIGINAL_MESSAGE_HANDLERS:
        dispatcher.addTelegramMessageHandler(h)

