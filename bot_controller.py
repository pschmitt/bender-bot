#!/usr/bin/python
# encoding: utf-8

dispatcher = None
ORIGINAL_MESSAGE_HANDLERS = None

def __remove_all_message_handlers():
    for h in dispatcher.telegram_message_handlers:
        dispatcher.removeTelegramMessageHandler(h)

def set_message_handler(handler):
    global ORIGINAL_MESSAGE_HANDLERS
    if ORIGINAL_MESSAGE_HANDLERS is None:
        ORIGINAL_MESSAGE_HANDLERS = list(dispatcher.telegram_message_handlers)
    __remove_all_message_handlers()
    dispatcher.addTelegramMessageHandler(handler)

def reset_message_handler():
    global ORIGINAL_MESSAGE_HANDLERS
    __remove_all_message_handlers()
    for h in ORIGINAL_MESSAGE_HANDLERS:
        dispatcher.addTelegramMessageHandler(h)
    ORIGINAL_MESSAGE_HANDLERS = None

