from flask_restful_helper import Manager
from apps.account.models import model


class User(Manager):
    _model = model.User



