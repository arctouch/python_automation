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
import yaml
from envyaml import EnvYAML

_PROJECT_ROOT = os.path.abspath(os.getcwd())
_DEFAULT_CONFIG_PATH = _PROJECT_ROOT + "/resources/app_config.yaml"
_SAUCE_LABS = True if bool(util.strtobool(os.environ['SAUCE_LABS'])) else False

with open(_DEFAULT_CONFIG_PATH) as config:
    _CONFIG_INFO = EnvYAML(_DEFAULT_CONFIG_PATH)
    _APP_CONFIG = _CONFIG_INFO['AppConfiguration']
    for platform in _APP_CONFIG:
        if 'app' in _APP_CONFIG[platform]:
            if _SAUCE_LABS:
                _APP_CONFIG[platform]["app"] = 'storage:filename={}'.format(str(_APP_CONFIG[platform]["app"]))
            else:
                _APP_CONFIG[platform]["app"] = _PROJECT_ROOT + '/resources/apps/' + str(_APP_CONFIG[platform]["app"])

print(_CONFIG_INFO.get('Appium'))
APPLICATION_CONFIG = _CONFIG_INFO['AppConfiguration']
APPIUM_CONFIG = _CONFIG_INFO.get('Appium')
MOCK_SERVER_CONFIG = _CONFIG_INFO.get('MockServer')
