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


class RunnerBase:
    def __init__(self, device_info, app_info, system_capabilities):
        caps = {}
        caps.update(system_capabilities)
        caps.update(device_info)
        caps.update(app_info)
        w3c = {
                'chromeOptions':
                    {
                        'w3c': False
                    }
            }
        self._capabilities = caps
        self._capabilities.update(w3c)
        self._system_capabilities = system_capabilities
        self._app_info = app_info
        self._device_info = device_info
        self._driver = None
        self._is_sauce_labs = True if bool(util.strtobool(os.environ['SAUCE_LABS'])) else False


    @property
    def driver(self):
        return self._driver

    @property
    def platform(self):
        raise Exception("Runners must define a `platform` property. Valid platform values are 'web', 'ios', 'android'")

    def prepare(self):
        pass

    def start(self):
        raise Exception("Runners must define a `start()` method")

    def reset(self):
        raise Exception("Runners must define a `reset()` method")

    def stop(self):
        raise Exception("Runners must define a `stop()` method")

    def quit(self):
        raise Exception("Runners must define a `quit()` method")


def runner_for(platform, device, app, system_capabilities):
    platform_name = device['platformName']
    runner_name = platform if platform else platform_name

    if runner_name == 'web' and platform_name != 'web':
        runner_name = 'web-mobile'

    assert runner_name, "Unable to determine platform runner to be used. Use '-D platform=<platform_name>' parameter when \
                    running the command or add 'platformName' property to the device in device_config.json"

    from . import RunnerIOS, RunnerAndroid, RunnerWeb, RunnerMobileWeb

    runners = {
        "web": RunnerWeb,
        "web-mobile": RunnerMobileWeb,
        "ios": RunnerIOS,
        "android": RunnerAndroid
    }

    assert runner_name in runners, f"No runner found for platform '{runner_name}'"

    runner = runners[runner_name](device, app[runner_name], system_capabilities)

    print(f'Using runner: {runner_name}')

    return runner
