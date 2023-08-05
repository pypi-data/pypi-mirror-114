#!/usr/bin/env python
# -*- coding:utf-8 -*-

from abc import ABC, abstractmethod


class Server(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def graceful_stop(self):
        pass

    @abstractmethod
    def run_forever(self):
        pass

    @abstractmethod
    def handle_term_signal(self):
        pass
