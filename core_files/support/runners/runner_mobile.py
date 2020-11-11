from appium import webdriver
from appium.webdriver.appium_service import AppiumService
from behave.model import Scenario

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
        self._start_appium_server_if_needed()

    def start(self):
        if not self._driver:
            port = str(self._capabilities["port"])
            self._driver = webdriver.Remote(f'http://localhost:{port}/wd/hub', self._capabilities)

    def reset(self):
        if self._driver:
            self._driver.reset()

    def stop(self):
        if self._driver:
            self._driver.terminate_app(self.app_id)

    def quit(self):
        if self._driver:
            self._driver.quit()

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
