from main.extension import ma
from apps.account.models import model


class User(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = model.User

    password = ma.Str(load_only=True)


class UserLogin(ma.Schema):
    username = ma.Str(required=True)
    password = ma.Str(required=True)


