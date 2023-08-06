from flask import jsonify
from flask import make_response as _make_response
from flask import abort as _abort
from flask_restful.utils import http_status_message


def abort(status_code, messages=None):
    if messages is None:
        messages = {'error': http_status_message(status_code)}
    response = make_response(success=False, data=messages, status_code=status_code)
    _abort(response)


def make_response(success, data, status_code):
    if success:
        response = data
    else:

        response = {
            'messages': data,
        }

    return _make_response(jsonify(response), status_code)
