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
from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from behave.model import Scenario
from selenium.common.exceptions import WebDriverException
from support.runners.runner import RunnerBase


class MobileRunnerBase(RunnerBase):

    def __init__(self, device_info, app_info, system_capabilities):
        super().__init__(device_info, app_info, system_capabilities)
        self._service = None


    @property
    def device_info(self):
        return self._device_info


    @property
    def app_info(self):
        return self._app_info


    @property
    def capabilities(self):
        return self._capabilities


    @property
    def app_id(self):
        raise Exception("Runner must implement 'app_id' property")


    def supports_scenario(self, scenario: Scenario):
        return True


    def prepare(self):
        if not self._is_sauce_labs:
            self._start_appium_server_if_needed()


    def start(self):
        self._driver = self.create_driver(saucelabs=self._is_sauce_labs)


    def reset(self):
        if self._driver:
            self._driver.reset()


    def stop(self):
        if self._driver:
            self._driver.quit()


    def quit(self):
        if self._driver:
            if not self._is_sauce_labs:
                pass

        if self._service:
            print("------ STOPPING APPIUM SERVER ------")
            self._service.stop()


    def _start_appium_server_if_needed(self):
        caps = self._capabilities
        port = caps['port']
        udid = caps['udid']
        system_port = caps['systemPort']

        server_running = self._check_server_running(port)
        if server_running:
            print(f"\n ℹ️ Using appium server at: host=127.0.0.1 port={port}\n")
            return

        print("\n------ LAUNCHING APPIUM SERVER ------\n")

        self._service = AppiumService()
        self._service.start(args=[
            '-U', str(udid),
            '-p', str(port),
            '--webdriveragent-port', str(system_port),
            '--allow-insecure', 'chromedriver_autodownload'
        ])

        print(f"Server started (host=127.0.0.1 port={port})")


    @staticmethod
    def _check_server_running(port, host='127.0.0.1'):
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host, port))
        sock.close()
        server_running = result == 0
        return server_running


    def create_driver(self, saucelabs=False):
        port = str(self._capabilities["port"])
        if saucelabs:
            access_key = str(self._capabilities['accessKey'])
            username = str(self._capabilities['username'])
            self._capabilities['name'] = 'Automated Test: {}'.format(self._capabilities['deviceName'])
            self._driver = webdriver.Remote(f'https://{username}:{access_key}@ondemand.us-west-1.saucelabs.com:443/wd/hub', self._capabilities)
            return self._driver
        else:
            if 'browserName' in self._capabilities:
                del self._capabilities['browserName']
            self._driver = webdriver.Remote(f'http://localhost:{port}/wd/hub', self._capabilities)
            return self._driver


    def send_status(self, status):
        try:
            self._driver.execute_script('sauce:job-result={}'.format(status))
        except (WebDriverException):
            pass
