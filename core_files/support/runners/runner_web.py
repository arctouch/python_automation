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
import re

from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager

from .runner import RunnerBase
import logging


class RunnerWeb(RunnerBase):

    def __init__(self, device_info, app_info, system_capabilities):
        super().__init__(device_info, app_info, system_capabilities)
        self._driver = None
        self._service = None

    @property
    def platform(self):
        return 'web'

    def start(self):
        self._driver = self._create_selenium_driver(self._capabilities['name'], self._capabilities['headless'])
        self._driver.maximize_window()
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

    @staticmethod
    def _create_selenium_driver(browser, headless=False):
        if browser == 'chrome-mac':
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.add_argument('window-size=1920,1080')
            return webdriver.Chrome(ChromeDriverManager(log_level=logging.ERROR).install(), options=options)
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
