#!/usr/bin/env python
import re
import requests
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import six
from subsfinder import __version__, __author__
version = __version__
author = __author__


if not version:
    raise RuntimeError('Cannot find version information')
if not author:
    raise RuntimeError('Cannot find author information')

requires = [
    'requests',
    'lxml',
    'bs4',
    'gevent',
    'rarfile',
    'six',
]


def readme():
    if six.PY2:
        with open('README.md') as fp:
            content = fp.read()
    else:
        with open('README.md', encoding='utf-8') as fp:
            content = fp.read()
    return content


setup(
    name='SubsFinder',
    version=version,
    author=author,
    author_email='wflc@163.com',
    description='subsfinder -- a general finder for subtitles',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/wflc/subsfinder/',
    keywords=['subtitle', 'subsfinder', 'sub', 'subtitle finder', 'shooter', 'zimuku'],
    license='MIT',
    packages=['subsfinder', 'subsfinder.subsearcher', 'subsfinder.tools'],
    include_package_data=True,
    python_requires='>=3',
    install_requires=requires,
    entry_points={
        'console_scripts': [
                'subsfinder = subsfinder.run_gevent:run',
                'subutils = subsfinder.utils:main'
        ]
    },
)
