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
import glob
import os
from os.path import join

import requests
from flask import Flask, request, jsonify, abort

from support.server_mock.response_coding import serialize_response, generate_response_key, deserialize_response

app = Flask(__name__)
_active_variant = None
_missing_variant_should_fallback = bool(os.getenv('MOCK_MISSING_VARIANT_FALLBACK', False))
_forward_requests = bool(os.getenv('MOCK_FORWARD_REQUESTS', False))
_record_responses = bool(os.getenv('MOCK_RECORD_RESPONSES', False))

_forward_to_server = str(os.getenv('MOCK_FORWARD_TO_SERVER', 'https://cat-fact.herokuapp.com/'))
MOCK_FILES_ROOT = join(os.getcwd(), 'server-mock')


@app.route('/mock', methods=['GET', 'POST', 'DELETE'])
def update_config():
    if request.method == 'DELETE':
        _reset_config()

    if request.method == 'POST':
        _handle_update_config_request(request)

    return _server_config()


@app.route('/mock/<string:config_key>', defaults={'path': ''}, methods=['GET', 'POST', 'DELETE'])
@app.route('/mock/<string:config_key>/<path:path>', methods=['GET', 'POST', 'DELETE'])
def set_variant(config_key, path):
    if request.method == 'DELETE':
        _reset_config(key=config_key)

    if request.method == 'POST':
        _handle_update_config_request(request, key=config_key)

    return _server_config(include=[config_key])


@app.route('/', defaults={'path': ''}, methods=['HEAD', 'GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['HEAD', 'GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    print(f"requested path: {path}")

    saved_response = _fetch_response(request)

    if saved_response is not None:
        return saved_response

    if not _forward_requests:
        return response_not_found()

    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, _forward_to_server),
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=True)

    _save_response(request, path, resp)

    return _fetch_response(request)


@app.errorhandler(404)
def response_not_found(error=None):
    message = {
        'status': 404,
        'message': f'No mock data found for path: {request.full_path}',
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


def _variant_not_found(error=None):
    message = {
        'status': 404,
        'message': f'No variant set!',
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


def _save_response(req, path, resp):
    directory = join(MOCK_FILES_ROOT, path)
    file_name = generate_response_key(req, _active_variant)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(f'{directory}/{file_name}.http', 'w') as outfile:
        outfile.write(serialize_response(resp))


def _fetch_response(req):
    global _active_variant
    return _retrieve_response(req, _active_variant)


def _retrieve_response(req, variant=None):
    response_file = _response_file_path(req, variant=variant)
    files = glob.glob(response_file)

    if len(files) == 0:
        if variant is None or not _missing_variant_should_fallback:
            return None

        return _retrieve_response(req)

    return deserialize_response(files[0])


def _response_file_path(req, variant):
    directory = join(MOCK_FILES_ROOT, req.path.strip('/'))
    response_key = generate_response_key(req, variant)
    file_name = f'{response_key}.http'
    response_file = join(directory, file_name)
    return response_file


def _server_config(include=None):
    info = {
        "activeVariant": _active_variant,
        "missingVariantShouldFallback": _missing_variant_should_fallback,
        "forwardRequests": _forward_requests,
        "recordResponses": _record_responses,
        "forwardToServer": _forward_to_server
    }

    if include is None:
        return info

    return {key: info[key] for key in include}


def _reset_config(key=None):

    def _reset_active_variant():
        global _active_variant
        _active_variant = None

    def _reset_missing_variant_should_fallback():
        global _missing_variant_should_fallback
        _missing_variant_should_fallback = False

    def _reset_forward_requests():
        global _forward_requests
        _forward_requests = False

    def _reset_record_responses():
        global _record_responses
        _record_responses = False

    def _reset_forward_to_server():
        global _forward_to_server
        _forward_to_server = "http://example.com/"

    reset_methods = {
        'activeVariant': _reset_active_variant,
        'missingVariantShouldFallback': _reset_missing_variant_should_fallback,
        'forwardRequests': _reset_forward_requests,
        'recordResponses': _reset_record_responses,
        'forwardToServer': _reset_forward_to_server
    }

    if key is None:
        for _, reset_method in reset_methods.items():
            reset_method()
    else:
        if key not in reset_methods:
            abort(400, f'Invalid configuration key: "{key}"')
        reset_methods[key]()


def _update_server_config(config: dict):
    global _active_variant
    global _missing_variant_should_fallback
    global _forward_requests
    global _record_responses
    global _forward_to_server

    _active_variant = config.get('activeVariant', _active_variant)
    _missing_variant_should_fallback = config.get('missingVariantShouldFallback', _missing_variant_should_fallback)
    _forward_requests = config.get('forwardRequests', _forward_requests)
    _record_responses = config.get('recordResponses', _record_responses)
    _forward_to_server = config.get('forwardToServer', _forward_to_server)


def _handle_update_config_request(req, key=None):
    if not request.is_json:
        abort(400, 'POST content is not a valid JSON')

    info = request.get_json()
    if key is None:
        _update_server_config(info)
        return

    if key not in info:
        abort(400, f'JSON content missing key "{key}"')

    value = info[key]
    types = {
        'activeVariant': str,
        'missingVariantShouldFallback': bool,
        'forwardRequests': bool,
        'recordResponses': bool,
        'forwardToServer': str
    }

    if type(value) is not types[key]:
        abort(400, f'"{key}" is not a valid {types[key]}.')

    _update_server_config(info)


if __name__ == '__main__':
    app.run()
