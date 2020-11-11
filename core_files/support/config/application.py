import os
import yaml

_PROJECT_ROOT = os.path.abspath(os.getcwd())
_DEFAULT_CONFIG_PATH = _PROJECT_ROOT + "/resources/app_config.yaml"

with open(_DEFAULT_CONFIG_PATH) as config:
    _CONFIG_INFO = yaml.load(config, Loader=yaml.FullLoader)
    _APP_CONFIG = _CONFIG_INFO['AppConfiguration']
    for platform in _APP_CONFIG:
        if 'app' in _APP_CONFIG[platform]:
            _APP_CONFIG[platform]["app"] = _PROJECT_ROOT + str(_APP_CONFIG[platform]["app"])

APPLICATION_CONFIG = _CONFIG_INFO['AppConfiguration']
APPIUM_CONFIG = _CONFIG_INFO.get('Appium')
MOCK_SERVER_CONFIG = _CONFIG_INFO.get('MockServer')
