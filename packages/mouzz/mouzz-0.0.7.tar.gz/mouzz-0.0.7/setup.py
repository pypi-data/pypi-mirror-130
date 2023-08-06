#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='mouzz',
    version='0.0.7',
    author='prim',
    author_email='1210102@qq.com',
    url='https://github.com/prim',
    description=u'mouzz',
    packages=['mouzz'],
    install_requires=["mouse", "keyboard", "psutil", "pywin32"],
	data_files=[('config', ['mouzz/config.json'])],
    entry_points={
        'console_scripts': [
            'mouzz=mouzz:main',
        ]
    }
)
