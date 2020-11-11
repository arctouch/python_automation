from . import MobileRunnerBase


class RunnerAndroid(MobileRunnerBase):

    @property
    def app_id(self):
        return self.capabilities['appPackage']

    @property
    def platform(self):
        return 'android'

    def start(self):
        super().start()
        self._driver.activate_app(self.app_id)

    def supports_scenario(self, scenario):
        return "Automation" in scenario.tags or "AutomationAndroid" in scenario.tags
