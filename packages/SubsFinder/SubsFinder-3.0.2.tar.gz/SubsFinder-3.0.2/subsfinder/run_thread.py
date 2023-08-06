# -*- coding: utf8 -*-
""" 命令行入口的多线程版本
"""
from .subfinder_thread import SubFinderThread as SubsFinder
from .run import run as run_


def run():
    run_(SubsFinder)


if __name__ == '__main__':
    run()
