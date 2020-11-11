import os
import json
import re
import subprocess
import configparser
from pathlib import Path

def get_relative_path(path):
    root = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
    return os.path.join(root, path)


def get_config_filepath():
    return get_relative_path('resources/device_config.json')

def run_commands(commands):
    output = subprocess.run(commands, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT).stdout.decode('utf-8')

    lines = output.split('\n')
    lines = [line for line in lines if line != '']
    return lines

def name_from_device(device_name):
    return device_name.replace('_', ' ')

def get_ios_devices_and_simulators():
    print('Searching for iOS physical devices and simulators...')

    lines = run_commands(['instruments', '-s', 'devices'])
    lines = lines[2:] # Removing first lines with "Known Devices:" and this computer
    lines = [line for line in lines if '+ Apple Watch' not in line] # Removing combinations of simulator and apple watch
    key_matcher = re.compile(r'\s*(?P<device_name>.*)\s\((?P<os_version>[0-9.]+)\)\s\[(?P<udid>[0-F-]+)\](\s\(.*\))?\s*$')

    devices = []
    for line in lines:
        match = key_matcher.match(line)
        if not match:
            continue

        device_name = match.group('device_name')
        name = name_from_device(device_name)
        os_version = match.group('os_version')
        udid = match.group('udid')

        device = {'name': name, 'deviceName': device_name, 'udid': udid, 'platformName': 'ios', 'platformVersion': os_version}
        devices.append(device)

    print('iOS devices found: {:d}\n'.format(len(devices)))
    return devices

def get_android_devices():
    print('Searching for Android physical devices...')

    lines = run_commands(['adb', 'devices'])
    lines = lines[1:] # Removing first line with "List of devices attached"
    key_matcher = re.compile(r'\s*(?P<udid>.*)\sdevice*$')

    udids = []
    for line in lines:
        match = key_matcher.match(line)
        if not match:
            continue

        udid = match.group('udid')
        if not udid.startswith('emulator-'):
            udids.append(udid)

    devices = []
    for udid in udids:
        commands = ['adb', '-s', udid, 'shell', 'getprop']
        name_commands = commands + ['ro.product.system.model']
        version_commands = commands + ['ro.system.build.version.release']

        error_message = 'Could not fetch information for Android device with UDID {}'.format(udid)

        try:
            device_name = run_commands(name_commands)[0]
            os_version = run_commands(version_commands)[0]
        except:
            print(error_message)
            continue

        if device_name == '' or os_version == '':
            print(error_message)
            continue

        name = name_from_device(device_name)
        device = {'name': name, 'deviceName': device_name, 'udid': udid, 'platformName': 'android', 'platformVersion': os_version}
        devices.append(device)

    print('Android devices found: {:d}\n'.format(len(devices)))
    return devices

def get_android_emulators():
    print('Searching for Android emulators...')
    device_names = run_commands(['emulator', '-list-avds'])

    version_ref = {}
    with open(get_relative_path('support/generator/android_version_reference.json')) as json_file:
        version_ref = json.load(json_file)

    devices = []
    for device_name in device_names:
        config_filepath = os.path.expanduser('~/.android/avd/{}.ini'.format(device_name))
        api_version = ''

        try:
            with open(config_filepath) as config_file:
                section = 'DEFAULT'
                config_with_default = '[{}]\n'.format(section) + config_file.read()
                config_data = configparser.ConfigParser()
                config_data.read_string(config_with_default)
                api_version = config_data[section]['target'].replace('android-', '')
        except:
            print('Could not fetch API version for Android emulator named {}'.format(device_name))
            continue

        os_version = version_ref[api_version]
        if os_version is None:
            print('Could not fetch OS version for Android emulator named {}'.format(device_name))
            continue

        name = name_from_device(device_name)
        udid = 'emulator-5554' # Android Virtual Device Manager always set a value for UDID with format "emulator-{port}", with port starting with 5554
        device = {'name': name, 'deviceName': device_name, 'udid': udid, 'platformName': 'android', 'platformVersion': os_version}
        devices.append(device)

    print('Android emulators found: {:d}\n'.format(len(devices)))
    return devices

def merge_devices(new_devices):
    existing_devices = []
    with open(get_config_filepath()) as json_file:
        existing_devices = json.load(json_file)['devices']

    def device_exists(device):
        udid = device['udid']
        filtered = ''
        for existing in existing_devices:
            if existing['platformName'] != 'web':
                if existing['udid'] == udid:
                    filtered = existing
        # filtered = [existing for existing in existing_devices if existing['udid'] == udid]
        if udid.startswith('emulator-'):
            for existing in existing_devices:
                if existing['platformName'] != 'web':
                    if existing['deviceName'] == device['deviceName'] and existing['platformVersion'] == device['platformVersion']:
                        filtered = existing
            # filtered = [existing for existing in existing_devices if existing['deviceName'] == device['deviceName'] and existing['platformVersion'] == device['platformVersion']]

        return len(filtered) > 0

    unmatched = [device for device in new_devices if not device_exists(device)]

    print('New devices added: {:d}'.format(len(unmatched)))
    return unmatched + existing_devices

def run():
    result = []
    result += get_ios_devices_and_simulators()
    result += get_android_devices()
    result += get_android_emulators()
    result = merge_devices(result)

    config_info = {"devices": result}
    config_data = json.dumps(config_info, indent=2)

    with open(get_config_filepath(), 'w') as json_file:
        json_file.write(config_data)

    print('Config file updated. Total of devices: {:d}'.format(len(result)))

if __name__ == '__main__':
    run()