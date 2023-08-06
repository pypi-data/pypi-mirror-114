import traceback

from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restful import Api as _Api
from flask_restful.utils import http_status_message
from jwt.exceptions import ExpiredSignatureError, DecodeError
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, MethodNotAllowed, HTTPException

from flask_restful_helper.response import make_response


class Api(_Api):
    def handle_error(self, e):
        """It helps preventing writing unnecessary
        try/except block though out the application
        """
        # Handle HTTPExceptions
        if isinstance(e, ValidationError):
            messages = e.normalized_messages()
            for key in messages.keys():
                messages[key] = messages[key][0]
            return make_response(False, messages, 400)
        elif isinstance(e, BadRequest):
            return make_response(False, e.data.get('message'), e.code)
        elif isinstance(e, MethodNotAllowed):
            return make_response(False, {'error': http_status_message(e.code)}, e.code)
        elif isinstance(e, AppException):
            return make_response(False, e.payload, e.status_code)

        elif isinstance(e, HTTPException):
            if hasattr(e, 'description') and e.description is not None:
                return make_response(False, getattr(e, 'description'), e.code)
        elif isinstance(e, IntegrityError):
            if e.orig.args[0] == 1062:
                return make_response(False, {'error': http_status_message(409)}, 409)
            elif e.orig.args[0] == 1451:
                return make_response(False, {'error': http_status_message(409)}, 409)
        elif isinstance(e, ExpiredSignatureError) or isinstance(e, NoAuthorizationError):
            return make_response(False, {'error': str(e)}, 401)
        elif isinstance(e, DecodeError):
            return make_response(False, {'error': str(e)}, 422)
        else:
            traceback.print_exc()

            # print(e.__dict__)

            return make_response(False, {'error': e}, 500)


class AppException(Exception):
    status_code = 500

    def __init__(self, payload=None, status_code=None):
        super(BaseException, self).__init__()
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return dict(self.payload or ())
