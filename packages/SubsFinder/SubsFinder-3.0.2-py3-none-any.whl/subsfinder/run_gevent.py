# -*- coding: utf8 -*-
""" 命令行入口的协程版本
"""

from .run import run as run_
from .subfinder_gevent import SubFinderGevent as SubsFinder
from gevent import monkey
monkey.patch_all()

def run():
    run_(SubsFinder)


if __name__ == '__main__':
    run()
