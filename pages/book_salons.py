#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .page import Page


class BookSalons(Page):

    def __init__(self, logger, driver, config):
        super(BookSalons, self).__init__(logger, driver, config)
        self.name = self.__class__.__name__

    def click_service_by_idx(self, row, group, item):
        selector = 'div:not(.container)>.row:nth-of-type(%d) .list-group:nth-of-type(%d)' \
                   ' .list-group-item:nth-of-type(%s)' % (row, group, item)
        self.click_by_css(selector)

        self.wait_for_element_by_css(".service-row")
        self.logger.info("service by idx: row: %d, group: %d, item in group: %d", row, group, item)

    def click_book_now(self, success=True):
        self.click_by_css(".btn-success")
        if success:
            self.wait_for_element_by_css('.modal[style="display: block;"]')