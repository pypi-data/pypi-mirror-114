from flask import Blueprint
from flask_restful import Api
from apps.account.api_views import api_view

blueprint = Blueprint('account', __name__, url_prefix='/account')
api = Api(blueprint)
api.add_resource(api_view.User, '/users', endpoint='users', methods=['GET', 'POST'])
api.add_resource(api_view.User, '/users/<pk>', endpoint='users_pk', methods=['GET', 'PUT', 'PATCH', 'DELETE'])


