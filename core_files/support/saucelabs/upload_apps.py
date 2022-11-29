import argparse
import os
import requests
from requests.structures import CaseInsensitiveDict
import base64
from pathlib import Path

url = "https://api.us-west-1.saucelabs.com/v1/storage/upload"
_PROJECT_ROOT = Path(Path(__file__).absolute()).parent.parent.parent
_FILES_PATH = os.path.join(_PROJECT_ROOT, 'resources/apps/')


def get_basic_auth():
    username = os.environ['SAUCE_USERNAME']
    access_token = os.environ['SAUCE_ACCESS_KEY']
    to_encode = f'{username}:{access_token}'
    to_encode_bytes = to_encode.encode('ascii')
    token = base64.b64encode(to_encode_bytes).decode('utf-8')
    return token


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--p', help='Example: $ upload_apps.py --p android | Insert the platform name.', required=True)
    parser.add_argument('--n', help='Example: $ upload_apps.py --p android --n prefix | Insert the prefix that will be used to distinguish this application in the SauceLabs file storage. Make sure to have your app_config.yml and name of file properly updated with prefix_android.apk', required=True)
    parser.add_argument('--l', help='Example: $ upload_apps.py --p android --l /Users/username/Desktop/android.apk | Insert the path to application. Missing this flag means that the applications should be located in /core_files/resources/apps folder.')
    parser.set_defaults(l=False)
    args = parser.parse_args()
    platform_name = args.p
    prefix = args.n
    custom_path = args.l

    assert platform_name=='android' or platform_name=='ios', 'Platform name should be android or ios'

    if platform_name=='android':
        platform_name = f'{prefix}_{platform_name}.apk'
    else:
        platform_name = f'{prefix}_{platform_name}.ipa'

    if not custom_path:
        path = _FILES_PATH + platform_name
    else:
        path = custom_path

    fields = {
        'payload': open(path, 'rb'),
        'name': f'{platform_name}',
        'description': f'{platform_name} build'
    }

    headers = CaseInsensitiveDict()
    headers["Authorization"] = f'Basic {get_basic_auth()}'

    resp = requests.post(url, headers=headers, files=fields)

    if resp.status_code > 300:
        print('////////////////////////////////')
        print('Something went wrong')
        print('////////////////////////////////')
        print(resp.status_code)
        print(resp.text)
    else:
        print('////////////////////////////////')
        print('The build was successfully uploaded.')
        print('////////////////////////////////')


if __name__ == '__main__':
    run()