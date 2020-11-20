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
import json

from flask import make_response, Response
from pathvalidate import sanitize_filename


def check_key_match(key):
    return True


def serialize_response(resp):
    headers = resp.headers
    content = resp.text

    if "application/json" in resp.headers.get("Content-Type", ""):
        content = json.dumps(resp.json(), indent=4)
        headers['Content-Length'] = len(content)

    formatted_headers = '\n'.join(
        [f'{name}: {value}' for name, value in headers.items() if name not in 'Content-Encoding']
    )

    content = '\n'.join([
        f'HTTP/{"{:.1f}".format(resp.raw.version / 10)} {resp.status_code} {resp.reason}',
        f'{formatted_headers}',
        '',
        f'{content}'
    ])

    return content


def generate_response_key(req, variant):
    variant_identifier = f'({variant.upper()})'.replace(' ', '_') if variant is not None else ''
    formatted_query = "".join([f'--{header}={value}' for header, value in sorted(req.args.items())])
    file_name = f'{req.method}{variant_identifier}{formatted_query}'

    return sanitize_filename(file_name)


def _read_content(file):
    return file.read().strip()


def _read_headers(file):
    headers = {}
    header = file.readline().strip()
    while len(header) > 0:
        key_value = header.split(": ")
        headers[key_value[0]] = key_value[1]
        header = file.readline().strip()

    return headers


def _read_status(file):
    status_info = file.readline()

    return int(status_info.split(" ")[1])


def deserialize_response(file):
    with open(file) as file:
        status = _read_status(file)
        headers = _read_headers(file)
        content = _read_content(file)

    response: Response = make_response(
        content,
        status
    )

    headers['Content-Length'] = len(content)

    response.headers = headers

    return response
