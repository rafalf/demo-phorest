#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .page import Page


class Signin(Page):

    def __init__(self, logger, driver, config):
        super(Signin, self).__init__(logger, driver, config)
        self.name = self.__class__.__name__

    def enter_email(self, value):
        selector = 'input[type="email"]'
        self.send_by_css(selector, value)
        self.logger.info("enter_email: " + value)

    def enter_password(self, value):
        selector = 'input[type="password"]'
        self.clear(selector)
        for c in value:
            self.send_by_css(selector, c, False)
        self.logger.info("enter_password: " + value)

    def click_btn_login(self, success=True):
        self.click_by_xpath("//button[contains(text(),'Login')]")
        if success:
            self.wait_for_element_by_xpath("//a[contains(text(),'Sign Out')]")
            self.logger.info("logged in ok")

    def click_btn_no_account(self):
        self.click_by_xpath("//button[contains(text(),'have an account')]")

        self.wait_for_element_by_css(".registration-form")
