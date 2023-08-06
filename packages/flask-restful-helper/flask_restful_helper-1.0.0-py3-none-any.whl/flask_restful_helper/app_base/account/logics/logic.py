from datetime import timedelta

from main.extension import bcrypt
from apps.account.managers import manager
from apps.account.schemas import schema
from flask_jwt_extended import create_access_token

from flask_restful_helper import Logic


class User(Logic):
    _manager = manager.User
    _schema = schema.User


class UserLogin(Logic):
    _manager = manager.User
    _schema = schema.UserLogin

    def create(self, data, query_args, *args, **kwargs):
        data = self.validate(data)
        user = self.manager.retrieve(login=data.get('username'))
        if user and bcrypt.check_password_hash(user.password, data.get('password')):
            user_claims = {'user': schema.User().dump(user)}
            obj = {
                'access_token': create_access_token(identity=user.id, expires_delta=timedelta(minutes=100),
                                                    additional_claims=user_claims)
            }
            return True, obj, 200
        else:
            return False, {'error': 'Username and password do not match or you do not have an account yet'}, 401
