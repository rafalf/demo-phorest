#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pytest
from config import *
import time
import random
import string
from datetime import datetime
import re


class Page(object):

    def __init__(self, logger, driver, config):
        self.logger = logger
        self.driver = driver
        self.config = config

        self.css = {
            "modalPrefix": '.modal[style="display: block;"] '
        }

        self.name = self.__class__.__name__
        self.wait = WebDriverWait(self.driver, 30)

    # pages
    def open_login_page(self):
        self.open_url(BASE_URL + self.config.get("append_login"))

    def open_signup_page(self):
        self.open_url(BASE_URL + self.config.get("append_signup"))

    # loggers
    def log_info(self, message):
        self.logger.info("%s: %s", self.name, message)

    def log_warning(self, message):
        self.logger.warning("%s: %s", self.name, message)

    def log_debug(self, message):
        self.logger.debug("%s: %s", self.name, message)

    def log_error(self, message):
        self.logger.error("%s: %s", self.name, message)

    def open_url(self, url):
        self.driver.get(url)

    def open_home(self):
        self.driver.get(BASE_URL)

    @property
    def get_today(self):
        return datetime.now().strftime("%b %d, %Y")

    @property
    def get_current_url(self):
        c = self.driver.current_url
        self.logger.info('current url: %s', c)
        return c

    @property
    def get_current_title(self):
        return self.driver.title

    def refresh_browser(self):
        self.driver.refresh()

    def get_random_string(self, chars=1):
        return "".join(random.choice(string.ascii_letters) for _ in range(chars))

    def get_random_str_number(self, digits=1):
        return "".join(str(random.randint(1, 10)) for _ in range(digits))

    @property
    def random_email(self):
        email = self.get_random_string(10) + "@toss.away"
        self.logger.info('random email: %s', email)
        return email

    @property
    def time_in_ms(self):
        millis = int(round(time.time() * 1000))
        return millis

    def delete_all_cookies(self):
        self.driver.delete_all_cookies()

    def clean_browser_storage(self):
        self.driver.execute_script('window.sessionStorage.clear();')
        self.driver.execute_script('window.localStorage.clear();')

    def get_alert_accept(self):

        alert = self.driver.switch_to_alert()
        alert_text = alert.text
        alert.accept()
        self.logger.info('alert: {}'.format(alert_text))
        return alert_text

    def wait_for_alert(self):
        WebDriverWait(self.driver, 60).until(EC.alert_is_present())

    def accept_alert_if_present(self):
        try:
            alert = self.driver.switch_to_alert()
            alert.accept()
        except:
            pass

    def is_alert_present(self):
        if EC.alert_is_present:
            return True

    def wait_for_windows(self, count):
        a = self.driver.window_handles
        for _ in range(10):
            if len(a) == count:
                self.logger.info('window count ok: %d', len(a))
                break
            else:
                self.logger.info('window count not yet: %d != %d', len(a), count)
                time.sleep(0.5)
        else:
            pytest.fail('wait_for_windows failed: {} != {]'.format(len(a), count))

    def get_current_window_handle(self):
        return self.driver.current_window_handle

    def switch_to_new_window(self):
        h = self.driver.window_handles[:-1]
        self.driver.switch_to.window(h)
        self.logger.info('switched to: %s', self.driver.title)

    def switch_to_main_window(self):
        h = self.driver.window_handles[0]
        self.driver.switch_to.window(h)
        self.logger.info('switched to: %s', self.driver.title)

    def wait_for_iframe(self):
        self.wait_for_element_by_css('iframe')

    def switch_to_iframe(self, frameName=""):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(frameName))

    def switch_to_stripe_frame(self):
        selector = "[name*='privateStripeFrame']"
        self.ensure_element_settles(selector)
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(self.driver.find_element_by_css_selector(selector)))

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def wait_for_url_to_be(self, url):
        try:
            self.wait.until(EC.url_to_be(url))
        except Exception as err:
            pytest.fail('%s: error: %s', err.__class__.__name__, err)

    def wait_for_url_contains(self, url):
        try:
            self.wait.until(EC.url_contains(url))
            # self.get_current_url
        except Exception as err:
            pytest.fail('%s: error: %s' % (err.__class__.__name__, err))
    # -----------------------------
    # waiters, getters & clickers
    # -----------------------------

    def get_element_clickable_by_css(self, selector):

        try:
            return self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                                                 ,'get_element_clickable_by_css: timed out on: %s' % selector)
        except Exception as err:
            pytest.fail('%s: error: %s' % (err.__class__.__name__, err))

    def get_element_clickable_by_xpath(self, selector):

        try:
            return self.wait.until(EC.element_to_be_clickable((By.XPATH, selector))
                                                 ,'get_element_clickable_by_xpath: timed out on: %s' % selector)
        except Exception as err:
            pytest.fail('%s: error: %s' % (err.__class__.__name__, err))

    def get_element_by_css(self, selector):

        try:
            return self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                                        ,'get_element_by_css: timed out on: %s' % selector)
        except Exception as err:
            pytest.fail('%s: error: %s' % (err.__class__.__name__, err))

    def wait_for_element_by_css(self, selector, visible=False):

        try:
            if visible:
                self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                                                        ,'wait_for_element_by_css (visible): timed out on: %s' % selector)
            else:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                                        ,'wait_for_element_by_css (presence): timed out on: %s' % selector)
        except Exception as err:
            pytest.fail('%s: error: %s' % (err.__class__.__name__, err))

    def wait_for_element_by_xpath(self, selector):

        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, selector))
                                                        ,'wait_for_element_by_xpath: timed out on: %s' % selector)
        except Exception as err:
            pytest.fail('%s: error: %s' % (err.__class__.__name__, err))

    def get_element_by_css_no_fail(self, selector, time_out=1):

        try:
            return WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        except:
            return None

    def get_all_elements_by_css(self, selector, time_out=30):

        try:
            return WebDriverWait(self.driver, time_out).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                                                 ,'get_all_elements_by_css: timed out on: %s' % selector)
        except Exception as err:
            pytest.fail('%s: error: %s' % (err.__class__.__name__, err))

    def get_all_elements_by_xpath(self, selector, time_out=30):

        try:
            return WebDriverWait(self.driver, time_out).until(EC.presence_of_all_elements_located((By.XPATH, selector))
                                                 ,'get_all_elements_by_xpath: timed out on: %s' % selector)
        except Exception as err:
            pytest.fail('%s: error: %s' % (err.__class__.__name__, err))

    def get_all_elements_by_css_no_fail(self, selector, time_out=1):
        try:
            return WebDriverWait(self.driver, time_out).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                                                 ,'get_all_elements_by_css_no_fail: timed out on: %s' % selector)
        except:
            return []

    def wait_until_element_not_present(self, selector, time_out=30, visible=False):

        try:
            if not visible:
                WebDriverWait(self.driver, time_out).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                                                 ,'wait_until_element_not_present (presence): timed out on: %s' % selector)
            elif visible:
                WebDriverWait(self.driver, time_out).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
                                                 ,'wait_until_element_not_present (visible): timed out on: %s' % selector)

        except Exception as err:
            pytest.fail('%s: error: %s' % (err.__class__.__name__, err))

    def ensure_element_not_present(self, selector):

        try:
            self.driver.find_element_by_css_selector(selector)
            pytest.fail('ensure_element_not_present failed: element %s found!' % selector)
        except:
            pass

    def is_element_by_css(self, selector_css, time_out=30, visible=False, clickable=False):

        try:
            if not visible and not clickable:
                WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, selector_css)), 'is_element_by_css (presence): element timed out: %s' % selector_css)
            elif visible:
                WebDriverWait(self.driver, time_out).until(EC.visibility_of_element_located((
                    By.CSS_SELECTOR, selector_css)), 'is_element_by_css (visibility): element timed out: %s' % selector_css)
            elif clickable:
                WebDriverWait(self.driver, time_out).until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, selector_css)), 'is_element_by_css (clickable): element timed out: %s' % selector_css)
            return True
        except:
            return None

    def is_element_by_xpath(self, xpath, time_out=30, visible=False, clickable=False):

        try:
            if not visible and not clickable:
                WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located((
                    By.XPATH, xpath)), 'is_element_by_xpath (presence): element timed out: %s' % xpath)
            elif visible:
                WebDriverWait(self.driver, time_out).until(EC.visibility_of_element_located((
                    By.XPATH, xpath)), 'is_element_by_xpath (visibility): element timed out: %s' % xpath)
            elif clickable:
                WebDriverWait(self.driver, time_out).until(EC.element_to_be_clickable((
                    By.XPATH, xpath)), 'is_element_by_xpath (clickable): element timed out: %s' % xpath)
            return True
        except:
            return None

    def click_by_css(self, selector):

        for _ in range(3):
            try:
                el = self.get_element_clickable_by_css(selector)
                el.click()
                return
            except Exception as err:
                self.logger.info('%s: error... retry in 1s', err.__class__.__name__)
                time.sleep(1)
        pytest.fail('click_by_css failed')

    def click_if_clickable(self, element):

        for _ in range(3):
            try:
                if element.is_enabled() and element.is_displayed():
                    element.click()
                    return
                else:
                    time.sleep(1)
            except Exception as err:
                self.logger.info('%s: error... retry in 1s', err.__class__.__name__)
                time.sleep(1)
        pytest.fail('click_by_css failed')

    def click_by_xpath(self, selector):

        for _ in range(3):
            try:
                el = self.get_element_clickable_by_xpath(selector)
                el.click()
                return
            except Exception as err:
                self.logger.info('%s: error... retry in 1s', err.__class__.__name__)
                time.sleep(1)
        pytest.fail('click_by_xpath failed')

    def clear(self, selector):
        el = self.get_element_by_css(selector)
        el.clear()

    def send_by_css(self, selector, value, clear=True):

        for _ in range(3):
            try:
                el = self.get_element_by_css(selector)
                if clear:
                    el.clear()
                el.send_keys(value)
                return
            except Exception as err:
                self.logger.info('%s: error... retry in 1s', err.__class__.__name__)
                time.sleep(1)
        pytest.fail('send_by_css failed')

    def get_href_attribute(self, selector):
        el = self.get_element_by_css(selector)
        return el.get_attribute('href')

    def table_cells(self, locator='table td'):
        self.wait_for_element_by_css(locator)
        a = self.get_all_elements_by_css(locator)
        cells = [e.text for e in a]
        return cells

    def ensure_no_error(self):
        self.wait_until_element_not_present(self.css['error'], 1)

    def ensure_element_settles(self, selector, sleep=1):
        position = dict()
        for idx in range(10):
            el = self.get_element_by_css(selector)
            if el.location == position:
                self.logger.info('position settled: %s', position)
                break
            else:
                if idx != 0:
                    self.logger.info('not settled yet: %s != %s', position, el.location)
                position = el.location
                time.sleep(sleep)

    def assert_tables(self, tbl1, tbl2):

        """
        to assert both tables are equal
        's:{}': skip
        'i:{}': assert in e.g cell1 = i:{2020} in 10.10.2020 would pass
        'b:{}': break
        """

        if "b:{}" not in tbl1 and "b:{}" not in tbl2:
            assert len(tbl1) == len(tbl2)

        for cell1, cell2 in zip(tbl1, tbl2):
            self.logger.info('cells: {} {}'.format(cell1, cell2))
            if cell1 == 's:{}' or cell2 == 's:{}':
                self.logger.info('assert skipped: cell found == s:{}')
            elif cell1.count('b:{}') or cell2 == 'b:{}':
                self.logger.info('assert completed: cell found == b:{}')
                return
            elif cell1.count('i:{'):
                cell_in = cell1[3:-1]
                self.logger.info('assert %s in %s:', cell_in, cell2)
                assert cell_in in cell2
            else:
                assert cell1 == cell2

    def assert_lists(self, lst1, lst2):

        """
        :param lst1: list no1
        :param lst2: list no2

        's:{}': skip
        'i:{}': assert in container e.g list el1 = i:{2020} in el2 = 10.10.2020 would pass
        note: lst2 is always a container
        """

        assert len(lst1) == len(lst2)

        for el1, el2 in zip(lst1, lst2):
            self.logger.info('elements lst1: {} lst2: {}'.format(el1, el2))
            if el1 == 's:{}' or el2 == 's:{}':
                self.logger.info('assert skipped: lst1 found == s:{}')
            elif el1.count('i:{'):
                el1 = el1[3:-1]
                self.logger.info('assert %s in %s:', el1, el2)
                assert el1 in el2
            else:
                assert el1 == el2

    def assert_match(self, pattern, string):

        """to assert regex pattern matches string"""

        search_obj = re.search(pattern, string, flags=0)
        if search_obj:
            self.logger.info('pattern: %s found in str: %s', pattern, string)
        else:
            raise AssertionError('pattern: {} not found in str: {}'.format(pattern, string))

    # js

    def click_js(self, css):
        exec_js = 'document.querySelector(\'{}\').click()'.format(css)
        self.driver.execute_script(exec_js)

    def scroll_into_view(self, css, offset_heading=True, fixed_by=None):

        self.wait_for_element_by_css(css)
        scroll_into_view = "document.querySelector('" + css + "').scrollIntoView();"
        self.driver.execute_script(scroll_into_view)

        if offset_heading and not fixed_by:
            offset_heading = "window.scrollBy(0, -150);"
            self.driver.execute_script(offset_heading)
        elif fixed_by:
            offset = "window.scrollBy({});".format(fixed_by)
            self.driver.execute_script(offset)

    def scroll_top_page(self):
        self.driver.execute_script('window.scrollTo(0, 0);')

    def set_js_value(self, css, value):
        exec_js = "document.querySelector('{}').value = '{}'".format(css, value)
        self.driver.execute_script(exec_js)

    # common

    def select_btn_book_now_modal(self):
        selector = self.css['modalPrefix'] + ".modal-footer button.btn-success"
        self.click_by_css(selector)

        active = ".bread-crumbs-choose-time.active"
        self.wait_for_element_by_css(active)

    def select_btn_add_more_services_modal(self):
        selector = self.css['modalPrefix'] + ".modal-footer button.btn-default"
        self.click_by_css(selector)

        self.wait_until_element_not_present(self.css['modalPrefix'])

    def ensure_confirm_active_breadcrumb(self):
        active = ".bread-crumbs-confirm.active"
        self.wait_for_element_by_css(active)

    def get_form_error(self):
        err = self.get_element_by_css(".has-error span").text
        self.logger.info("get_form_error: %s", err)
        return err

    def ensure_no_form_error(self):
        self.wait_until_element_not_present("#has-error")




