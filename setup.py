#!/usr/bin/env python3

'''Telegram Bot Notifier distribution script'''

from setuptools import setup

setup(
    name='tbnotify',
    version='0.1',
    description=__doc__,
    packages=['tbnotify'],
    entry_points={
        'console_scripts': [
            'tbnotify_server=tbnotify.server:main',
            'tbnotify_send=tbnotify.send:main'
        ]
    }
)