from flask import Flask

from main.extension import db, api, cors, migrate, ma, db_helper, jwt, bcrypt
from app.router import registry_router
from app.setting import Setting

def create_app(config_type):
    app = Flask(__name__)
    app.config.update(Setting(config_type).to_dict())
    db.init_app(app)
    db_helper.init_app(app, db)
    api.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    registry_router(app)

    for rule in app.url_map.iter_rules():
        print(rule)

    return app
