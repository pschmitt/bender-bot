#!/usr/bin/python
# coding: utf-8

from types import FunctionType


def remove_first_word(string):
    return ' '.join(string.split()[1:])

def first_word(string):
    return string.partition(' ')[0]

def public_defs(module):
    '''
    Get all public methods of a module
    '''
    return [x for x,y in module.__dict__.items() if type(y) == FunctionType]
