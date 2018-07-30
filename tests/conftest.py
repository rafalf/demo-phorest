import sys
import os
ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

import pytest
from selenium import webdriver
from config import BASE_DIR, BASE_URL, LOGGING_CONFIG, DOWNLOAD_DIR
import os
from sys import platform
import logging
import logging.config
import yaml


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="browser: chrome, firefox.")
    parser.addoption("--logger", action="store", default="DEBUG", help="logger level.")
    parser.addoption("--config", action="store", default='config.yaml', help="path to config.yaml")


@pytest.fixture()
def driver():

    global BROWSER

    BROWSER = pytest.config.getoption("--browser")

    print("[INFO] browser: {}".format(BROWSER))

    if BROWSER == 'chrome':
        options = chrome_options()
        if platform == 'darwin':
            wd = webdriver.Chrome(chrome_options=options)
        elif platform == 'linux' or platform == 'linux2':
            wd = webdriver.Chrome(chrome_options=options)
        else:
            chrome_path = os.path.join(BASE_DIR, 'drivers', 'chromedriver.exe')
            wd = webdriver.Chrome(executable_path=chrome_path, chrome_options=options)
    else:
        pytest.fail("[ERROR] unrecognized browser: {}".format(BROWSER))

    wd.get(BASE_URL)
    yield wd
    #  teardown
    wd.quit()


@pytest.fixture()
def config():
    fp = pytest.config.getoption("--config")
    if fp == 'config.yaml':
        fp = os.path.join(BASE_DIR, "config.yaml")
    with open(fp, 'r') as yaml_file:
        return yaml.load(yaml_file)


@pytest.fixture()
def logger():
    LEVEL = pytest.config.getoption("--logger")
    print("[INFO] Logger: {}".format(LEVEL))
    logging.config.dictConfig(LOGGING_CONFIG)
    log = logging.getLogger('main')
    log.setLevel(level=logging.getLevelName(LEVEL))
    return log


def chrome_options(caps=False):
    opts = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "credentials_enable_service": False,
        "password_manager_enabled": False
    }
    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--window-size=1440,900")
    if caps:
        return opts.to_capabilities()
    else:
        return opts

