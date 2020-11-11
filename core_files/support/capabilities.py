import json

def fetch_device_info(device_name):
    """Parses the "device_config.json" file to a valid dict object
    Creates a dict with the specified device_name, if the same is specified on
    the "device_config.json" file.
    It will always use a property specified in the device object with higher
    priority than the properties outside of it. This makes it really easy to
    set different app locations for devices that need different binaries, for
    example a simulator.
    """
    device_name = device_name.replace("_", " ")

    with open('resources/device_config.json', 'r') as f:
        device_config = json.load(f)

    return next((device for device in device_config['devices'] if device['name'] == device_name), None)
