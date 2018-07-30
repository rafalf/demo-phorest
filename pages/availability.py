#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .page import Page


class Availability(Page):

    def __init__(self, logger, driver, config):
        super(Availability, self).__init__(logger, driver, config)
        self.name = self.__class__.__name__

    def click_available_time(self, sign_in=True):
        selector = '.availability-date .btn-sm'
        self.click_by_css(selector)

        if sign_in:
            self.wait_for_element_by_css(".sign-in-form")
