#!/usr/bin/python
# coding: utf-8

def remove_first_word(string):
    return ' '.join(string.split()[1:])

def first_word(string):
    return string.partition(' ')[0]
