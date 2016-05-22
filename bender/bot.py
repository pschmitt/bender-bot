#!/usr/bin/python
# coding: utf-8

from __future__ import unicode_literals
import abc

class Bot():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def handle_message(self, sender, text):
        pass

    @abc.abstractmethod
    def send_text_message(self, recipient, text):
        pass

    @abc.abstractmethod
    def send_picture(self, recipient, image):
        pass

