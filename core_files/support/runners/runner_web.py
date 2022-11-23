# Copyright 2020 ArcTouch LLC (authored by Thiago Werner at ArcTouch)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
from distutils import util
import os
import re

from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.remote.remote_connection import RemoteConnection
from .runner import RunnerBase
import logging
from selenium.common.exceptions import WebDriverException


class RunnerWeb(RunnerBase):

    def __init__(self, device_info, app_info, system_capabilities):
        super().__init__(device_info, app_info, system_capabilities)
        self._driver = None
        self._service = None


    @property
    def platform(self):
        return 'web'


    def start(self):
        self._driver = self.create_selenium_driver(self._capabilities, self._app_info, self._device_info)
        self._driver.maximize_window()
        self._driver.set_window_size(1920, 1080)
        address = self._capabilities['address']
        address_format = re.compile('^http(s)?://')

        assert address_format.match(address), f"The web `address` must include the protocol (http:// or https://). " \
                                              f"Found: '{address}' "

        self._driver.get(address)


    def reset(self):
        pass


    def stop(self):
        self._driver.close()


    def quit(self):
        self._driver.quit()


    @staticmethod
    def supports_scenario(scenario):
        return "Automation" in scenario.tags or "AutomationWeb" in scenario.tags


    def create_selenium_driver(self, capabilities, app_info, device_info):
        browser = capabilities['name']
        headless = capabilities['headless']

        if self._is_sauce_labs:
            test_name = 'Web Test Automation {}'.format(browser)
            caps = {
                'sauce:options': {
                    'username': capabilities['username'],
                    'accessKey': capabilities['accessKey'],
                    'name': test_name
                }
            }
            caps.update(app_info)
            caps.update(device_info)
            if browser == 'FirefoxWindows' or browser == 'ChromeWindows':
                selenium_endpoint = "https://ondemand.us-west-1.saucelabs.com/wd/hub"
            elif browser == 'FirefoxLinux' or browser == 'ChromeLinux':
                selenium_endpoint = "https://ondemand.us-east-1.saucelabs.com:443/wd/hub"
            else:
                assert False, 'This browser is not supported by SauceLabs.'
            executor = RemoteConnection(selenium_endpoint)
            return webdriver.Remote(executor, desired_capabilities=caps)
        else:
            if 'appPackage' in capabilities:
                del capabilities['appPackage']
            if browser == 'chrome-mac':
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument('window-size=1920,1080')
                return webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=options)
            elif browser == 'firefox-mac':
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument('window-size=1920,1080')
                return webdriver.Firefox(executable_path=GeckoDriverManager(log_level=logging.ERROR).install(), options=options)
            elif browser == 'safari':
                return webdriver.Safari(executable_path='/usr/bin/safaridriver')
            elif browser == 'ie11':
                return webdriver.Ie(IEDriverManager(log_level=logging.ERROR).install())
            elif browser == 'edge':
                return webdriver.Edge(EdgeChromiumDriverManager(log_level=logging.ERROR).install())


    def send_status(self, status):
        try:
            self._driver.execute_script('sauce:job-result={}'.format(status))
        except (WebDriverException):
            pass
