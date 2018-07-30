#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .page import Page


class Register(Page):

    def __init__(self, logger, driver, config):
        super(Register, self).__init__(logger, driver, config)
        self.name = self.__class__.__name__

    def enter_name(self, value):
        selector = 'input[placeholder="Full Name"]'
        self.send_by_css(selector, value)
        self.logger.info("enter_name: " + value)

    def enter_email(self, value):
        selector = 'input[placeholder="Email"]'
        self.send_by_css(selector, value)
        self.logger.info("enter_email: " + value)

    def enter_mobile(self, value):
        selector = 'input[placeholder="Mobile Phone Number"]'
        self.send_by_css(selector, value)
        self.logger.info("enter_mobile: " + value)

    def enter_password(self, value):
        selector = 'input[placeholder="Password"]'
        self.send_by_css(selector, value)
        self.logger.info("enter_password: " + value)

    def click_btn_signup(self):
        self.click_by_xpath("//button[contains(text(),'Sign up')]")

