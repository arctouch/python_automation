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
import json
import os
from unittest.mock import patch

from behave import fixture, use_fixture
from behave.log_capture import capture

from support.capabilities import fetch_device_info
from support.config.application import APPIUM_CONFIG, APPLICATION_CONFIG
from support.config.application import MOCK_SERVER_CONFIG

from support.model.user import User
from support.reporters.junit import JUnitReporter
# -- FILE: features/environment.py
# USE: behave -D BEHAVE_DEBUG_ON_ERROR         (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=yes     (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=no      (to disable debug-on-error)
from support.runners.runner import runner_for
from support.server_mock.mock_server import MockServerRequestHandler
from support.constants.mocks.endpoints import PATHS

BEHAVE_DEBUG_ON_ERROR = False
APPIUM_DEFAULT_PORT = 4723
APPIUM_DEFAULT_SYSTEM_PORT = 8200


@fixture
def valid_user(context, *args, **kwargs):
    """
    Use this method in case the application has a default valid credentials.
    """
    context.user = User(
        username="standard_user",
        password="secret_sauce"
    )
    return context.user


@fixture
def setup_mock_responses(context, *args, **kwargs):
    endpoint = os.environ['API_ENDPOINT']
    path = PATHS[endpoint]['PATH']
    mock_config_url = 'http://localhost:{port}/{path}'.format(port=context.port, path=path)

    with patch.dict('support.constants.mocks.endpoints.__dict__', {PATHS[endpoint]['URL']: mock_config_url}):
        return


def _setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")


def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb
        ipdb.post_mortem(step.exc_traceback)


def before_all(context):
    print("BEFORE_ALL")

    TASK_ID = int(os.environ['TASK_ID']) if 'TASK_ID' in os.environ else 0

    try:
        SAUCE_LABS = bool(util.strtobool(os.environ['SAUCE_LABS']))
    except:
        SAUCE_LABS = False

    context.is_sauce_labs = True if bool(util.strtobool(os.environ['SAUCE_LABS'])) else False

    _setup_debug_on_error(context.config.userdata)
    """Start the appium client and set some env variables"""
    """The code is using the default_port 4723 to initialize the first webdriver/device."""
    """Both default_port and systemPort are being increased based on the task_id number."""
    """So, the task_id number is a integer number that increases as much as devices we're using to automate."""

    assert 'device' in context.config.userdata, "'device' parameter is missing. (-D device=\"Device Name\")"
    context.device_name = context.config.userdata['device']

    context.platform = context.config.userdata.get('platform')

    junit_reporter = JUnitReporter(context)
    context.config.reporters.append(junit_reporter)

    device_info = fetch_device_info(context.device_name)

    assert device_info is not None, f"No info found in config file for device '{context.device_name}'"

    system_capabilities = {
        "port": APPIUM_DEFAULT_PORT + TASK_ID,
        "systemPort": APPIUM_DEFAULT_SYSTEM_PORT + TASK_ID,
        "processArguments": {
            "args": []
        }
    }

    if SAUCE_LABS:
        sauce_caps = {
            "username": APPIUM_CONFIG['username'],
            "accessKey": APPIUM_CONFIG['accessKey']
        }
        system_capabilities.update(sauce_caps)

    context = _start_mock_server(context, MOCK_SERVER_CONFIG)

    print('\n------ SETTING UP AUTOMATION ------\n')
    context.runner = runner_for(platform=context.platform, device=device_info, app=APPLICATION_CONFIG,
                                system_capabilities=system_capabilities)

    if hasattr(context.runner, "capabilities"):
        print(f'Capabilities: \n{json.dumps(context.runner.capabilities, indent=4)}')

    context.runner.prepare()
    context.add_cleanup(context.runner.quit)
    print('\n------ STARTING TESTS ------\n')


def _start_mock_server(context, server_info):
    host = server_info['host']
    context.port = server_info['port']
    context = MockServerRequestHandler.start_mock_server(context, host, context.port)

    print(f'\n------ STARTING MOCK SERVER ------\n')

    if _check_server_running(host=host, port=context.port):
        print(f'Existing server found (host={host} port={context.port})')
    
    return context


def _stop_mock_server_if_needed(context):
    if hasattr(context, 'mock_server'):
        print(f'\n------ STOPPING MOCK SERVER ------\n')
        MockServerRequestHandler.stop_serving()


def _check_server_running(port, host='127.0.0.1'):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    sock.close()
    server_running = result == 0
    return server_running


@capture
def after_all(context):
    print(f"AFTER_ALL :: Test execution complete ({context.device_name})")
    _stop_mock_server_if_needed(context)


def after_scenario(context, scenario):
    """Closes the app after each test"""
    if context.is_sauce_labs:
        context.runner.send_status(scenario.status)

    context.runner.stop()


def before_scenario(context, scenario):
    """
    Opens the app before each scenario.
    If it's a new feature, the newfeature tag will reset the app. The newfeature tag is totally optional.
    """
    if "continue_on_error" in scenario.tags:
        scenario.continue_after_failed_step = True

    use_fixture(valid_user, context, timeout=10)
    
    context.runner.start()


def before_feature(context, feature):
    for scenario in feature.scenarios:
        scenario.name = f"{scenario.name} ({context.device_name})"

        if not context.runner.supports_scenario(scenario):
            scenario.mark_skipped()


def after_feature(context, feature):
    pass


def before_step(context, step):
    pass


def before_tag(context, tag):
    if tag == "valid_user":
        use_fixture(valid_user, context, timeout=10)
    if tag == 'configuration':
        os.environ['API_ENDPOINT'] = 'configuration'
        use_fixture(setup_mock_responses, context, timeout=10)
