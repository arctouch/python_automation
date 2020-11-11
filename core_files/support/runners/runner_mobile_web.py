from selenium import webdriver

from . import MobileRunnerBase


class RunnerMobileWeb(MobileRunnerBase):

    def start(self):
        super().start()
        self._driver.get(self._capabilities['address'])

    @property
    def platform(self):
        return 'web'

    def stop(self):
        self._driver.close()
