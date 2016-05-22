#!/usr/bin/env python
# coding: utf-8

from abc import ABCMeta, abstractmethod


class ChatPlugin():

    __metaclass__ = ABCMeta

    @abstractmethod
    def response(self, sender):
        pass
