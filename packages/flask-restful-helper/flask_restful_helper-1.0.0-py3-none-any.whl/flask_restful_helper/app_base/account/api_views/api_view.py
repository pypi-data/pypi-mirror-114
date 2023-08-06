from flask_restful_helper import ApiView
from apps.account.logics import logic
from flask_jwt_extended import jwt_required


class User(ApiView):
    _logic = logic.User
    decorators = [jwt_required()]

    """
    可重寫 GET POST PUT PATCH DELETE Function
    """