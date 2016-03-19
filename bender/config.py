#!/usr/bin/python
# coding: utf-8

import yaml

def get_config(config_file='../bender.yaml'):
    with open(config_file) as f:
        config = yaml.load(f)
    return config

def get_config_section(config_file='../bender.yaml', section='bot'):
    return get_config(config_file)[section]

def get_token(config_file='../bender.yaml'):
    return get_config_section(config_file, 'bot')['token']

def get_authorized_users(config_file='../bender.yaml'):
    return get_config_section(config_file, 'bot')['authorized_users']

