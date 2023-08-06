#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
It is aimed to produce solutions for Thread and Multi Process operations.
"""

__author__ = 'ibrahim CÖRÜT'
__email__ = 'ibrhmcorut@gmail.com'

from threading import Thread
from time import time


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=True):
        self.__target = None
        self.__args = None
        self.__kwargs = None
        self.__return = None
        self.__elapsed_time = None
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

    def run(self):
        print(f'~~~~~~~ THREAD STARTED ~~~~~~~ Name:{self.name}')
        self.__elapsed_time = time()
        if self.__target is not None:
            self.__return = self.__target(*self.__args, **self.__kwargs)

    def stop(self, *args):
        if self.__target is not None:
            Thread.join(self, *args)
        print(
            f'~~~~~~~ THREAD STOPPED ~~~~~~~ Name:{self.name}:--->{time() - self.__elapsed_time}'
        )
        return self.__return
