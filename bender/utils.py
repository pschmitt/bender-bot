#!/usr/bin/python
# coding: utf-8

from types import FunctionType
import random
import socket


def remove_first_word(string):
    return ' '.join(string.split()[1:])

def first_word(string):
    return string.partition(' ')[0]

def public_defs(module):
    '''
    Get all public methods of a module
    '''
    return [x for x,y in module.__dict__.items() if type(y) == FunctionType]

def check_port(host, port, timeout=0.2):
    '''
    Check whether we can connect to a specific host on a specific port
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, int(port)))
        return True
    except:
        return False

def random_local_port():
    '''
    Get a random port that is free to use
    '''
    while True:
        random_port = random.randint(1025, 65535)
        if not check_port('127.0.0.1', random_local_port):
            return random_port

def fuzzy_find_key(d, k):
    '''
    Find a key inside a dict, independently of its character case
    '''
    for key in d.keys():
        if key == k:
            return k
        if key.lower() == k or key.lower() == k.lower():
            return key.lower()
