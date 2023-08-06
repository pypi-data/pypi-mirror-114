# -*- coding: utf8 -*-
""" 命令行入口的协程版本
"""

from gevent import monkey
monkey.patch_all()
from .subfinder_gevent import SubFinderGevent as SubsFinder
from .run import run as run_


def run():
    run_(SubsFinder)


if __name__ == "__main__":
    run()
