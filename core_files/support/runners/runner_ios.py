from . import MobileRunnerBase


class RunnerIOS(MobileRunnerBase):

    @property
    def app_id(self):
        return self.capabilities['bundleIdentifier']

    @property
    def platform(self):
        return 'ios'

    def start(self):
        super().start()
        self._driver.activate_app(self.app_id)

    def supports_scenario(self, scenario):
        return "Automation" in scenario.tags or "AutomationIOS" in scenario.tags
