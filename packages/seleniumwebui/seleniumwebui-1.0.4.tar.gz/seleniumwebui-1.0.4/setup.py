#-*- coding:utf8 -*-
'''
Created on 2021年7月30日

@author: perilong
'''

from setuptools import setup

setup(
    name='seleniumwebui',
    version='1.0.4',
    description='selenium-web-ui-test-tool, need pywin32 for selenium3',
    author='perilong',
    author_email='357858088@qq.com',
    packages=['seleniumWebUi'],
    install_requires=['selenium==3.141.0', 'pyperclip==1.8.2', 'pywin32'],
    )