#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='zf_sampleSprider',
    version='0.2.0',
    author='zhangfan',
    author_email='1054934500@qq.com',
    url='https://github.com/ilovepythonJAVAc/test2020_8_4',
    description='简易爬虫',
    packages=['sampleSprider_old','sampleSprider_old.Common'],
    install_requires=[
        'requests>=2.25.1',
        'beautifulsoup4>=4.9.3',
        'selenium>=3.141.0',
        'lxml>=4.6.3'
    ],
    entry_points={
        'console_scripts': [
            'fiction=sampleSprider_old.SampleSprider3_Fiction:main',
            'comics=sampleSprider_old.SampleSprider4_Comics1:main'
        ]
    }
)