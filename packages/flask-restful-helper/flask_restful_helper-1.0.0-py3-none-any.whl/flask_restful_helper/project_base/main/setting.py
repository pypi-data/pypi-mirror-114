from pathlib import Path

import yaml
from tests.enumerations import RoleType


class Setting(object):

    def __init__(self, config_type):
        with open(Path.cwd().joinpath('config', f'{config_type}.yaml'), 'r', encoding='utf-8') as f:
            env = yaml.load(f.read(), Loader=yaml.CLoader)

        self.config = self._build_config(env)

    def _build_config(self, env):
        config = dict()
        config['DEBUG'] = env['DEBUG']
        config['SQLALCHEMY_DATABASE_URI'] = env['SQLALCHEMY_DATABASE_URI']
        config['SQLALCHEMY_TRACK_MODIFICATIONS'] = env['SQLALCHEMY_TRACK_MODIFICATIONS']
        config['JWT_SECRET_KEY'] = env['JWT_SECRET_KEY']
        config['IS_NEED_INIT_DB_EVERY_TEST'] = env['IS_NEED_INIT_DB_EVERY_TEST']
        config['DB_CONN_HOST'] = env['DB_CONN_HOST']
        config['DB_CONN_PORT'] = env['DB_CONN_PORT']
        config['DB_CONN_USER'] = env['DB_CONN_USER']
        config['DB_CONN_PASSWORD'] = str(env['DB_CONN_PASSWORD'])
        config['DB_CONN_DB'] = env['DB_CONN_DB']
        for attr, value in RoleType.__dict__.items():
            if not attr.startswith('__'):
                config[value + '_USERNAME'] = env[value + '_USERNAME']
                config[value + '_PASSWORD'] = env[value + '_PASSWORD']
        return config

    def to_dict(self):
        return self.config
