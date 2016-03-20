#!/usr/bin/python
# coding: utf-8

import pkgutil
import importlib

def __get_all_plugins():
    return [name for _, name, _ in pkgutil.iter_modules(['plugins']) if name != 'sample']

def get_command_text(prefix=''):
    plugins = __get_all_plugins()
    register = ''
    for p in plugins:
        l = importlib.import_module('plugins.{}.{}'.format(p, p))
        for cmd, value in l.COMMANDS.iteritems():
            register += '{}{} - {}'.format(prefix, cmd, value['description'])
            if 'aliases' in value:
                aliases = value['aliases']
                register += ' (Aliases: '
                for a in aliases:
                    register += a
                    if a == aliases[-1]:
                        register += ')'
                    else:
                        register += ', '
            # if cmd != l.COMMANDS.keys()[-1]:
            register += '\n'
    return register

def get_help_text():
    cmd_help = get_command_text(prefix='/')
    return '/help - Help\n{}'.format(cmd_help)

def register():
    # TODO Messge @BotFather with this text
    print(get_command_text())

if __name__ == '__main__':
    register()
