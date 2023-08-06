# -*- coding: utf8 -*-
""" SunFinder 的协程版本
"""

from __future__ import unicode_literals
from gevent.pool import Pool
from .subsfinder import SubsFinder


class SubFinderGevent(SubsFinder):
    """ SubsFinder Thread version
    """

    def _init_pool(self):
        self.pool = Pool(10)
