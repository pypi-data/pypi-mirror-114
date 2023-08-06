#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='circle-douya', # 项目的名称,pip3 install get-time
    version='0.0.1', # 项目版本
    author='douya', # 项目作者
    author_email='1664619362@qq.com', # 作者email
    url='https://github.com/qumeili/circle_douya', # 项目代码仓库
    description='画圆', # 项目描述
    packages=['get_circle'], # 包名
    install_requires=[],
    entry_points={
        'console_scripts': [
            'get_circle=get_circle:zfx', # 使用者使用get_time时,就睡到get_time项目下的__init__.py下执行get_time函数
        ]
    } # 重点
)