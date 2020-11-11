import json
import os
import shlex
import signal
import subprocess
from os.path import join

from behave import fixture, use_fixture
from behave.log_capture import capture

from support.capabilities import fetch_device_info
from support.config.application import APPLICATION_CONFIG
from support.config.application import MOCK_SERVER_CONFIG
from support.model.user import User
from support.reporters.junit import JUnitReporter
# -- FILE: features/environment.py
# USE: behave -D BEHAVE_DEBUG_ON_ERROR         (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=yes     (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=no      (to disable debug-on-error)
from support.runners.runner import runner_for

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

    _start_mock_server(context, TASK_ID)

    print('\n------ SETTING UP AUTOMATION ------\n')
    context.runner = runner_for(platform=context.platform, device=device_info, app=APPLICATION_CONFIG,
                                system_capabilities=system_capabilities)

    if hasattr(context.runner, "capabilities"):
        print(f'Capabilities: \n{json.dumps(context.runner.capabilities, indent=4)}')

    context.runner.prepare()
    context.add_cleanup(context.runner.quit)
    print('\n------ STARTING TESTS ------\n')


def _start_mock_server(context, task_id=0, server_info=MOCK_SERVER_CONFIG):
    host = server_info['host']
    port = server_info['port'] + task_id

    print(f'\n------ STARTING MOCK SERVER ------\n')

    if _check_server_running(host=host, port=port):
        print(f'Existing server found (host={host} port={port})')
        return

    my_env: dict = {
        'FLASK_APP': join(os.getcwd(), 'support/server_mock/server_mock.py'),
        'FLASK_ENV': 'development',
        'FLASK_DEBUG': '1'
    }

    if 'forwardToServer' in server_info:
        my_env['MOCK_FORWARD_TO_SERVER'] = server_info['forwardToServer']

        if server_info['forwardRequests']:
            my_env['MOCK_FORWARD_REQUESTS'] = '1'
        if server_info['recordResponses']:
            my_env['MOCK_RECORD_RESPONSES'] = '1'

    if server_info['missingVariantFallback']:
        my_env['MOCK_MISSING_VARIANT_FALLBACK'] = '1'

    command = f'automation_virtualenv/bin/python -m flask run --host={host} --port={port}'
    print(f'{command}')

    context.mock_server_process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE, env=my_env, preexec_fn=os.setsid)

    context.add_cleanup(_stop_mock_server_if_needed, context)


def _stop_mock_server_if_needed(context):
    if hasattr(context, 'mock_server_process'):
        print(f'\n------ STOPPING MOCK SERVER ------\n')
        os.killpg(os.getpgid(context.mock_server_process.pid), signal.SIGTERM)  #


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


def after_scenario(context, scenario):
    """Closes the app after each test"""
    context.runner.stop()


def before_scenario(context, scenario):
    """
    Opens the app before each scenario.
    If it's a new feature, the newfeature tag will reset the app. The newfeature tag is totally optional.
    """
    if "continue_on_error" in scenario.tags:
        scenario.continue_after_failed_step = True

    if "continuation" not in scenario.tags:
        context.runner.reset()

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
