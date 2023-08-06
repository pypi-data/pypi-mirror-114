from pathlib import Path

import yaml


class Setting(object):

    def __init__(self, config_type):
        with open(Path.cwd().joinpath('config', f'{config_type}.yaml'), 'r', encoding='utf-8') as f:
            env = yaml.load(f.read(), Loader=yaml.CLoader)

        self.config = self._build_config(env)

    def _build_config(self, env):
        config = dict()
        config['DEBUG'] = env['DEBUG']
        config['DB'] = env['DB']
        config['DB_TYPE'] = db_type = config['DB'].get('DB_TYPE')
        config['DB_USERNAME'] = db_username = config['DB'].get('DB_USERNAME')
        config['DB_PASSWORD'] = db_password = config['DB'].get('DB_PASSWORD')
        config['DB_HOST'] = db_host = config['DB'].get('DB_HOST')
        config['DB_PORT'] = db_port = config['DB'].get('DB_PORT')
        config['DB_DATABASE'] = db_database = config['DB'].get('DB_DATABASE')
        if db_type == 'mysql':
            config['SQLALCHEMY_DATABASE_URI'] = \
                f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"
        elif db_type == 'sqlite':
            config['SQLALCHEMY_DATABASE_URI'] = \
                f"sqlite:///sqlite.db"
        config['SQLALCHEMY_TRACK_MODIFICATIONS'] = env['SQLALCHEMY_TRACK_MODIFICATIONS']
        config['JWT_SECRET_KEY'] = env['JWT_SECRET_KEY']
        config['TEST_INIT_DB_ON_TEST'] = env['TEST_INIT_DB_ON_TEST']
        config['TEST_ACCOUNT'] = env['TEST_ACCOUNT']

        return config

    def to_dict(self):
        return self.config
